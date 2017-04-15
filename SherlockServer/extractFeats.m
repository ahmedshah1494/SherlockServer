function extractFeats(filelist)
    f = fopen(filelist,'r');
    while ~feof(f)
        line = fgets(f);
        extractFeat(strcat('E:/Downloads/QSIURP2016/SherlockServer/SherlockServer/',line));
    end
end

function extractFeat(file)
    display(file);
    [y,Fs] = audioread(file);
    [m,n] = size(y);
    y = y(1:min(m,132300));
    if (m < 2048)
        return
    end
    display(file);
    if ~(exist(strcat(file,'.mfcc64ms'), 'file') == 2)
        hamming = @(N)(0.54-0.46*cos(2*pi*[0:N-1].'/(N-1)));                
        [CCs,FBEs,frames] = mfcc(y,Fs,64,32,0.97,hamming,[50 15000],20,20,22);
        dlmwrite(strcat(file,'.mfcc64ms'),CCs);
    end
    if ~(exist(strcat(file,'.stft'), 'file') == 2)
        s = spectrogram(y,2822,1411,2048);
        s2 = abs(s);
        dlmwrite(strcat(file,'.stft'),s2);
    end
end
        
        