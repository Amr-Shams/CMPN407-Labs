```c

function main()
    clear all;
    close all;
    clc;

    N = 10;
    bits = generateBits(N);

    % Plot the bits
    plotBits(bits);
    Eb = 1;
    T = 1;
    fc = 1;
    SNR_dB = 1:10;
    SNR = 10.^(SNR_dB/10);
    No = Eb./SNR;

    % Generate signal and symbols
    [t, signal, s1, s2] = generateSignal(bits, Eb, T, fc, N);

    % Plot symbols
    plotSymbols(t, s1, s2);

    % Generate and plot noise for all SNR levels
    noise = generateNoise(t, No);
    plotNoise(t, noise, SNR_dB);

    % Generate and plot received signal for all SNR levels
    received_signal = generateReceivedSignal(signal, noise);
    plotReceivedSignal(t, received_signal, SNR_dB);

    % Generate and plot the BER vs EB/No 
    simulateBPSKModulation(N);

    % Save all figures
    saveAllFigures();
end

function bits = generateBits(N)
    bits = randi([0 1], 1, N);
end

function plotBits(bits)
    figure;
    subplot(2, 1, 1);
    stem(bits);
    title('Bits');
    hold on;
    saveFigure('Bits');
end

function [t, signal, s1, s2] = generateSignal(bits, Eb, T, fc, N)
    t = linspace(0, N*T, length(bits)*100);
    Q1 = cos(2*pi*fc*t)/sqrt(T/2);
    s1 = sqrt(Eb)*Q1;
    s2 = -sqrt(Eb)*Q1;

    signal = generateBPSKSignal(bits, s1, s2, t, N);
    
    % Plot the signal
    subplot(2, 1, 2);
    plot(t, signal);
    title('Signal');
    saveFigure('Signal');
end

function signal = generateBPSKSignal(bits, s1, s2, t, N)
    signal = [];
    for i = 1:N
        if bits(i) == 0
            signal = [signal s1(1:length(t)/N)];
        else
            signal = [signal s2(1:length(t)/N)];
        end
    end
end

function plotSymbols(t, s1, s2)
    figure;
    subplot(2, 1, 1);
    plot(t, s1);
    hold on;
    plot(t, s2);
    title('Symbols');
    saveFigure('Symbols');
end

function noise = generateNoise(t, No)
    noise = [];
    for i = 1:length(No)
        % Generate white Gaussian noise with zero mean and variance No/2
        noise_i = sqrt(No(i)/2) * (randn(1, length(t)) + 1j * randn(1, length(t)));
        noise = [noise; noise_i];
    end
end

function plotNoise(t, noise, SNR_dB)
    figure;
    for i = 1:length(SNR_dB)
        subplot(5, 2, i);
        plot(t, real(noise(i, :)));
        title(['Noise for SNR = ' num2str(SNR_dB(i)) ' dB']);
    end
    saveFigure('Noise');
end

function received_signal = generateReceivedSignal(signal, noise)
    received_signal = signal + noise;
end

function plotReceivedSignal(t, received_signal, SNR_dB)
    figure;
    for i = 1:length(SNR_dB)
        subplot(5, 2, i);
        plot(t, received_signal(i, :));
        title(['Received signal for SNR = ' num2str(SNR_dB(i)) ' dB']);
    end
    saveFigure('ReceivedSignal');
end

function simulateBPSKModulation(N)
    N = 48000;
    ip = rand(1, N) > 0.5;
    s = 2 * ip - 1;
    n = 1/sqrt(2) * (randn(1, N) + 1j * randn(1, N));
    Eb_N0_dB = 1:10;
    [simBer, theoryBer] = simulateBPSKModulationWithAWGN(s, n, Eb_N0_dB, N,ip);

    % Plot bit error probability curve for BPSK modulation
    figure;
    semilogy(Eb_N0_dB, theoryBer, 'b.-');
    hold on;
    semilogy(Eb_N0_dB, simBer, 'mx-');
    axis([1 10 10^-5 0.5]);
    grid on;
    legend('Theory', 'Simulation');
    xlabel('Eb/No, dB');
    ylabel('Bit Error Rate');
    title('Bit Error Probability Curve for BPSK Modulation');
    saveFigure('BERvsEbNo');
end

function [simBer, theoryBer] = simulateBPSKModulationWithAWGN(s, n, Eb_N0_dB, N,ip)
    simBer = zeros(size(Eb_N0_dB));
    theoryBer = 0.5 * erfc(sqrt(10.^(Eb_N0_dB/10)));

    for ii = 1:length(Eb_N0_dB)
        % Noise addition
        y = s + 10^(-Eb_N0_dB(ii)/20)*n;

        % Receiver - hard decision decoding
        ipHat = real(y) > 0;

        % Counting the errors
        nErr = size(find([ip - ipHat]), 2);
        simBer(ii) = nErr / N;
    end
end

function saveFigure(name)
    saveas(gcf, name, 'png');
end

function saveAllFigures()
    figHandles = findall(0, 'Type', 'figure');
    for i = 1:length(figHandles)
        figure(figHandles(i));
        saveFigure(['Figure_' num2str(i)]);
    end
end

```
