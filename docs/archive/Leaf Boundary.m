clc 
clear all
close all
leaves= imread('leaf.jpg');

%% Extract each color Next we using indexing to extract three 2D matrices
%from the 3D image data corresponding to the red, green, and blue components of the image%
r = leaves(:, :, 1);
g = leaves(:, :, 2);
b = leaves(:, :, 3);
figure %View different color planes
subplot(2,2,1),imshow(r),title('R Plane')
subplot(2,2,2),imshow(g),title('G Plane')
subplot(2,2,3),imshow(b),title('B Plane')
%% Calculate Green Then we perform an arithmetic operation on the matrices as
%a whole to try to create one matrix that represents an intensity of green.%
justGreen = g - r/2 - b/2;
%imshow(justGreen)
%% 
close all
%Threshold the image Now we can set a threshold to separate the parts of
%the image that we consider to be green from the rest.%
bw = justGreen > 30;
%imshow(bw)
%% Remove small unwanted objects%
close all
bw1 = bwareaopen(bw, 30);
%imshow(bw1)
% morfolojik dzeltme
se = strel('disk', 10); % resimdeki yapran byklne gre deer deimeli, byk deer ayrntlar bozuyor
bw2 = imclose(bw1, se);
%imshow(bw2)
%% yeil ksm ayrlm resmin binary grnts ile birleimi
%bw3 = im2bw(bw,0.01); 
%bw3 = bw3 | bw2
bw3 = imclose(bw3, se);%morfolojik kapama
imshow(bw3)
%% Filling holes of the image
fillResim = imfill(bw3,'holes'); 
imshow(fillResim)
%% edge detection
close all
edges= edge(fillResim);
imshow(edges),title(' kenarlar ')
