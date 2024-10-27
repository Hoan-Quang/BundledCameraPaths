% Bundled Camera Path Video Stabilization
% Written by Tan SU
% contact: sutank922@gmail.com

%clear all;
addpath('mesh');
addpath('RANSAC');
addpath('mex');



%% hanled
inputDirOri = 'D:/Dai_hoc/Nam5_Ky1/STP/VidStab/dataset/Bundled/images/Regular/';
outputDirOri = 'D:/Dai_hoc/Nam5_Ky1/STP/VidStab/dataset/Bundled/results/Regular/';
fid = fopen('D:/Dai_hoc/Nam5_Ky1/STP/VidStab/dataset/Bundled/results/Regular/time.txt', 'a');
for index = 40:40
    tic;
    %% Parametres
    % -------INPUT-------
    inputIdx = [num2str(index-1), '/'];
    inputDir = fullfile(inputDirOri, inputIdx);
    outputDir = fullfile(outputDirOri, inputIdx);
    if ~exist(outputDir, 'dir')
        mkdir(outputDir);
    end
    
    nFrames =  length(dir(strcat(inputDir,'*.png')));
    %resize = [720 1280];           % resize the input frame to this size. If input frame size is too large, rendering time might be very slow (MATLAB interp2 is too slow)
    % -------TRACK-------
    TracksPerFrame = 512;           % number of trajectories in a frame, 200 - 2000 is OK
    % -------STABLE------
    MeshSize = 12;                   % The mesh size of bundled camera path, 6 - 12 is OK
    Smoothness = 3;                 % Adjust how stable the output is, 0.5 - 3 is OK
    Span = 30;                      % Omega_t the window span of smoothing camera path, usually set it equal to framerate
    Cropping = 1;                   % adjust how similar the result to the original video, usually set to 1
    Rigidity = 2;                   % adjust the rigidity of the output mesh, consider set it larger if distortion is too significant, [1 - 4]
    iteration = 20;                 % number of iterations when optimizing the camera path [10 - 20]
    % -------OUTPUT------
    OutputPadding = 200;            % the padding around the video, should be large enough. 

    %% Track by KLT
    fprintf('\nTrack by KLT\n');
    %tic;
    track = GetTracks(inputDir, MeshSize, TracksPerFrame, nFrames); 
    %toc;

    %% Compute original camera path (by As-similar-as-possible Warping)
    fprintf('\nCompute original camera path\n');
    %tic;
    path = getPath(MeshSize, track);    
    %toc;

    %% Optimize the paths
    fprintf('\nOptimize the paths\n');
    %tic;
    bundled = Bundled(inputDir, path, Span, Smoothness, Cropping, Rigidity);
    bundled.optPath(iteration);
    %toc;

    %% Render the stabilzied frames
    fprintf('\nRender the stabilzied frames\n');
    %tic;
    bundled.render(outputDir, OutputPadding);
    %toc;

    %% End
    elapsedTime = toc;
    fprintf('\nEnd!\n');
    fprintf(fid, '%d: %.6f\n', index - 1, elapsedTime);
end 

fclose(fid);
