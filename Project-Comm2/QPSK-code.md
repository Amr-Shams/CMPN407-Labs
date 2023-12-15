```c
clear all;
close all;

% QPSK Modulation and Demodulation without consideration of noise
N = 10;
data = round(rand(1, N)); % Generating 0,1 with equal probability
figure(1)


stem(data, 'linewidth', 3), grid on;
title('Information before Transmitting');
axis([0 11 0 1.5]);

data_NZR = 2 * data - 1; % Data Represented at NZR form for QPSK modulation
s_p_data = reshape(data_NZR, 2, length(data)/2);  % S/P conversion of data

br = 10^6; % Transmission bit rate  1000000
f = br; % Minimum carrieشr frequency
T = 1/br; % Bit duration
t = T/99:T/99:T; % Time vector for one bit information

% QPSK modulation
y = [];
y_in = [];
y_qd = [];
for i = 1:length(data)/2
    y1 = s_p_data(1, i) * cos(2 * pi * f * t); % Inphase component
    y2 = s_p_data(2, i) * sin(2 * pi * f * t); % Quadrature component
    y_in = [y_in y1]; % Inphase signal vector
    y_qd = [y_qd y2]; % Quadrature signal vector
    y = [y y1 + y2]; % Modulated signal vector
end

Tx_sig = y; % Transmitting signal after modulation
tt = T/99:T/99:(T*length(data))/2;
figure(2)
subplot(3,1,1);
plot(tt, y_in, 'linewidth', 3), grid on;
title('Waveform for Inphase component in QPSK modulation');
xlabel('time (sec)');
ylabel('amplitude (volt)');

subplot(3,1,2);
plot(tt, y_qd, 'linewidth', 3), grid on;
title('Waveform for Quadrature component in QPSK modulation');
xlabel('time (sec)');
ylabel('amplitude (volt)');

subplot(3,1,3);
plot(tt, Tx_sig, 'r', 'linewidth', 3), grid on;
title('QPSK modulated signal (sum of Inphase and Quadrature phase signal)');
xlabel('time (sec)');
ylabel('amplitude (volt)');

% QPSK demodulation
Rx_data = [];
Rx_sig = Tx_sig; % Received signal
for i = 1:1:length(data)/2
    % Inphase coherent detector
    Z_in = Rx_sig((i-1)*length(t)+1:i*length(t)) .* cos(2 * pi * f * t);
    Z_in_intg = (trapz(t, Z_in)) * (2/T); % Integration using trapezoidal rule
    Rx_in_data = Z_in_intg > 0; % Decision Maker

    % Quadrature coherent detector
    Z_qd = Rx_sig((i-1)*length(t)+1:i*length(t)) .* sin(2 * pi * f * t);
    Z_qd_intg = (trapz(t, Z_qd)) * (2/T); % Integration using trapezoidal rule
    Rx_qd_data = Z_qd_intg > 0; % Decision Maker

    Rx_data = [Rx_data Rx_in_data Rx_qd_data]; % Received Data vector
end

figure(3)
stem(Rx_data, 'linewidth', 3) 
title('Information after Receiving');
axis([0 11 0 1.5]), grid on;

% QPSK Modulation with consideration of noise
N = 48e3;
EbNoDB = 0:1:10;
EbNo = 10.^(EbNoDB/10);
ber = zeros(size(EbNo));

for i = 1:length(EbNo)
    si = 2 * (round(rand(1, N)) - 0.5);
    sq = 2 * (round(rand(1, N)) - 0.5);
    s = si + 1j * sq;
    w = 1/sqrt(2 * EbNo(i)) * (randn(1, N) + 1j * randn(1, N));
    r = s + w;
    sih = sign(real(r));
    sqh = sign(imag(r));
    berReal = (N - sum(si == sih)) / N;
    berImag = (N - sum(sq == sqh)) / N;
    ber(i) = mean([berReal berImag]);
end

% Plotting
figure;
semilogy(EbNoDB, ber, '-o');
grid on;
xlabel('Eb/No (dB)');
ylabel('BER');
title('QPSK Modulation');
hold on;

% Theoretical BER
berTheory = 0.5 * erfc(sqrt(EbNo));
semilogy(EbNoDB, berTheory, 'r');
legend('Simulation', 'Theory', 'Location', 'Best');
hold off;
% Save all figures
 saveAllFigures();
function saveAllFigures()
    figHandles = findall(0, 'Type', 'figure');
    for i = 1:length(figHandles)
        figure(figHandles(i));
        saveFigure(['Figure_' num2str(i)]);
    end
end
```