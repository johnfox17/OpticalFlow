function [] = FirstDerivativeOfImage(x_derivative_path, y_derivative_path, image_path, threshold, thinned, compare)
    %derivatives = csvread('derivatives_x_std.txt');
    
    %Load Peridynamic Derivative Matrices
    x_derivative = csvread(x_derivative_path);
    y_derivative = csvread(y_derivative_path);
    
    %Load image to derive
    I = imread(image_path);
    Img = rgb2gray(I);
    [height,length] = size(Img);
    
    %Reshaping arrays
    x_der = reshape(x_derivative, height, length);
    y_der = reshape(y_derivative, height, length);
    
    %Thresholding derivatives
    x_der(x_der>abs(threshold))=1;
    y_der(y_der>abs(threshold))=1;
    x_der(x_der~=1)=0;    
    y_der(y_der~=1)=0;
    
    %Finding edges with both derivatives
    ImgEdges_x = x_der.*double(Img);
    ImgEdges_y = y_der.*double(Img);
    ImgEdges_x(ImgEdges_x~=0)=1;
    ImgEdges_y(ImgEdges_y~=0)=1;
    
    %Thinning the edges
    if thinned == true
        ImgEdges_x = bwmorph(ImgEdges_x, 'thin', inf);
        ImgEdges_y = bwmorph(ImgEdges_y, 'thin', inf);
    end
    ImgEdgesSum = ImgEdges_x+ImgEdges_y;
    %Plots
    figure; imshow(Img);
    title('Original Image')
    figure; imshow(ImgEdges_x);
    title('X Derivative')
    figure; imshow(ImgEdges_y);
    title('Y Derivative')
    figure; imshow(ImgEdgesSum);
    title('X Derivative and Y Derivative')
    
    if compare == true
        BW1 = edge(Img,'Canny');
        figure; imshowpair(ImgEdgesSum,BW1,'montage')
        title('PDDO vs Canny')
        BW2 = edge(Img,'Prewitt');
        figure; imshowpair(ImgEdgesSum,BW2,'montage')
        title('PDDO vs Prewitt')
    end
end