#include <opencv2/opencv.hpp>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <vector>
#include <string>

namespace py = pybind11;

// Yardımcı fonksiyon: cv::Mat'ı py::array_t<uint8_t>'e çevirir
py::array_t<uint8_t> mat_to_array(cv::Mat mat) {
  cv::Mat temp;
  if (mat.channels() == 1) {
    temp = mat;
  } else {
    cv::cvtColor(mat, temp, cv::COLOR_BGR2RGB);
  }
  py::array_t<uint8_t> result({temp.rows, temp.cols, temp.channels()});
  auto buf = result.request();
  std::memcpy(buf.ptr, temp.data, temp.total() * temp.elemSize());
  return result;
}

// Görüntüyü adım adım işleyip tüm aşamaları dönen fonksiyon
py::dict process_leaf_pipeline(const std::string &image_path) {
  py::dict pipeline;

  // 1. Orijinal Resmi Oku
  cv::Mat img = cv::imread(image_path, cv::IMREAD_COLOR);
  if (img.empty()) {
    throw std::runtime_error("Gorsel bulunamadi: " + image_path);
  }
  pipeline["1_original"] = mat_to_array(img);

  // 2. Renk Ayrıştırma (LAB + ExG)
  cv::Mat lab_img;
  cv::cvtColor(img, lab_img, cv::COLOR_BGR2Lab);
  std::vector<cv::Mat> channels;
  cv::split(lab_img, channels);
  cv::Mat a_channel = channels[1];

  cv::split(img, channels);
  cv::Mat b_f, g_f, r_f;
  channels[0].convertTo(b_f, CV_32F);
  channels[1].convertTo(g_f, CV_32F);
  channels[2].convertTo(r_f, CV_32F);
  cv::Mat exg = 2.0f * g_f - r_f - b_f;
  cv::normalize(exg, exg, 0, 255, cv::NORM_MINMAX);
  exg.convertTo(exg, CV_8U);

  cv::Mat green_mask;
  cv::bitwise_and(255 - a_channel, exg, green_mask);
  pipeline["2_color_mask"] = mat_to_array(green_mask);

  // 3. Threshold ve Morfoloji (Mesafe Öncesi Temizlik)
  cv::Mat bw;
  cv::threshold(green_mask, bw, 0, 255, cv::THRESH_BINARY | cv::THRESH_OTSU);
  cv::Mat kernel = cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(3, 3));
  cv::Mat opening;
  cv::morphologyEx(bw, opening, cv::MORPH_OPEN, kernel, cv::Point(-1, -1), 2);
  pipeline["3_cleaned_mask"] = mat_to_array(opening);

  // 4. Mesafe Dönüşümü (Distance Transform)
  cv::Mat dist_transform;
  cv::distanceTransform(opening, dist_transform, cv::DIST_L2, 5);
  cv::Mat dist_vis;
  cv::normalize(dist_transform, dist_vis, 0, 255, cv::NORM_MINMAX);
  dist_vis.convertTo(dist_vis, CV_8U);
  pipeline["4_distance_map"] = mat_to_array(dist_vis);

  // 5. Kesin Bölge (Sure Foreground / Background)
  double maxVal;
  cv::minMaxLoc(dist_transform, nullptr, &maxVal);
  cv::Mat sure_fg;
  cv::threshold(dist_transform, sure_fg, 0.4 * maxVal, 255, 0);
  sure_fg.convertTo(sure_fg, CV_8U);
  
  cv::Mat sure_bg;
  cv::dilate(opening, sure_bg, kernel, cv::Point(-1, -1), 3);

  cv::Mat unknown;
  cv::subtract(sure_bg, sure_fg, unknown);
  pipeline["5_foreground_seeds"] = mat_to_array(sure_fg);

  // 6. Watershed Markerları
  cv::Mat markers;
  int n_comp = cv::connectedComponents(sure_fg, markers);
  markers = markers + 1;
  for (int i = 0; i < unknown.rows; i++) {
    for (int j = 0; j < unknown.cols; j++) {
      if (unknown.at<uint8_t>(i, j) == 255) markers.at<int32_t>(i, j) = 0;
    }
  }

  // Renkli marker görselleştirme
  cv::Mat markers_vis;
  markers.convertTo(markers_vis, CV_8U, 10); // Her bileşene fark edilebilir renk ver
  pipeline["6_watershed_markers"] = mat_to_array(markers_vis);

  // 7. Watershed ve Sonuç
  cv::watershed(img, markers);
  
  cv::Mat final_edges = cv::Mat::zeros(img.size(), CV_8U);
  for (int i = 0; i < markers.rows; i++) {
    for (int j = 0; j < markers.cols; j++) {
      if (markers.at<int32_t>(i, j) == -1) final_edges.at<uint8_t>(i, j) = 255;
    }
  }
  cv::dilate(final_edges, final_edges, cv::getStructuringElement(cv::MORPH_RECT, cv::Size(2, 2)));
  pipeline["7_final_edges"] = mat_to_array(final_edges);

  return pipeline;
}

PYBIND11_MODULE(leaf_vision, m) {
  m.doc() = "C++ ve OpenCV tabanli ileri duzey yaprak analiz modulu";
  m.def("process_leaf", &process_leaf_pipeline, "Yaprak analizini adim adim yapar");
}