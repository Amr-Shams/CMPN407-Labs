```c
clear;

%% --- 8-PSK Modulation --- %%

N_8PSK = 48000;

% Generate random bits

random_bits_binary = randi([0, 1], 1, N_8PSK);

% Parameters for 8-PSK modulation

Eb_8PSK = 1/3;

Eo_8PSK = Eb_8PSK * 3;

no_of_symbols_8PSK = 8;

no_of_bits_in_symbol_8PSK = 3;

% Define 8-PSK constellation

mapped_bits_8PSK = [0 0 0; 1 1 0; 0 1 1; 1 0 1; 0 0 1; 0 1 0; 1 1 1; 1 0 0];

mapped_symbols_8PSK = [sqrt(Eo_8PSK) -sqrt(Eo_8PSK) 1j*sqrt(Eo_8PSK)...

-1j*sqrt(Eo_8PSK) sqrt(Eo_8PSK/2)*(1+1j) sqrt(Eo_8PSK/2)*(-1+1j)...

sqrt(Eo_8PSK/2)*(-1-1j) sqrt(Eo_8PSK/2)*(1-1j)];

% Map bits to symbols

mapped_8PSK = zeros(1, N_8PSK/no_of_bits_in_symbol_8PSK);

counter = 1;

for i = 1:no_of_bits_in_symbol_8PSK:N_8PSK

for count = 1:no_of_symbols_8PSK

if isequal(random_bits_binary(i:i+2), mapped_bits_8PSK(count, :))

mapped_8PSK(counter) = mapped_symbols_8PSK(count);

end

end

counter = counter + 1;

end

%% --- Channel Noise --- %%

SNR = 1:10;

BER_8PSK = zeros(1, length(SNR));

% Initialize subplot for displaying samples

figure('Name', '8-PSK Modulation and Demodulation');

subplot(2, 1, 1);

title('8-PSK Modulation: Random Samples');

% Plot some random samples before adding noise

plot(real(mapped_8PSK), imag(mapped_8PSK), 'o');

xlabel('In-Phase');

ylabel('Quadrature');

plotConstellation8PSK(mapped_symbols_8PSK, '8-PSK Constellation');

for i = 1:length(SNR)

% Add noise to the signal

No_8PSK = Eb_8PSK / 10^(SNR(i) / 10);

noise = randn(1, length(mapped_8PSK)) + 1j * randn(1, length(mapped_8PSK));

signal_8PSK_after_channel = mapped_8PSK + noise * sqrt(No_8PSK / 2);

% --- 8-PSK Demodulation --- %

demapped_bits_8PSK = demodulate_8PSK(signal_8PSK_after_channel, mapped_symbols_8PSK, mapped_bits_8PSK);

% Calculate Bit Error Rate

number_of_bit_errors = random_bits_binary - demapped_bits_8PSK;

BER_8PSK(i) = sum(abs(number_of_bit_errors)) / N_8PSK;

end

% Tight bound BER of 8-PSK

theoretical_BER_8PSK = 1/3 * erfc((sqrt(10.^(SNR/10))) * sqrt(3) * sin(pi/8));

% Subplot for displaying samples after adding noise

subplot(2, 1, 2);

title('8-PSK Demodulation: Samples After Adding Noise');

hold on;

% Plot some random samples after adding noise

plot(real(signal_8PSK_after_channel), imag(signal_8PSK_after_channel), 'x');

xlabel('In-Phase');

ylabel('Quadrature');

% Plotting BER vs Eb/N0

figure('Name', 'BER vs Eb/N0');

semilogy(SNR, BER_8PSK, 'r', 'LineWidth', 2);

hold on;

semilogy(SNR, theoretical_BER_8PSK, 'Color', 'k', 'LineStyle', '--', 'LineWidth', 2);

xlabel('SNR = Eb/No (dB)');

ylabel('BER');

grid on;

title('BER vs Eb/N0');

legend('8-PSK BER', 'Tight bound 8-PSK BER');

% save all figures

saveAllFigures();

function demapped_bits_8PSK = demodulate_8PSK(signal_8PSK_after_channel, mapped_symbols_8PSK, mapped_bits_8PSK)

demapped_bits_8PSK = zeros(1, length(signal_8PSK_after_channel) * 3);

counter = 1;

for j = 1:length(signal_8PSK_after_channel)

array_of_distances_8PSK = zeros(1, 8);

for count = 1:length(mapped_symbols_8PSK)

array_of_distances_8PSK(count) = abs(signal_8PSK_after_channel(j) - mapped_symbols_8PSK(count));

end

[~, index] = min(array_of_distances_8PSK);

demapped_bits_8PSK(counter:counter + 2) = mapped_bits_8PSK(index, :);

counter = counter + 3;

end

end

function saveAllFigures()

figHandles = findall(0, 'Type', 'figure');

for i = 1:length(figHandles)

figure(figHandles(i));

saveFigure(['Figure_' num2str(i)]);

end

end

function plotConstellation8PSK(mapped_symbols_8PSK, titleText)

figure;

plot(real(mapped_symbols_8PSK), imag(mapped_symbols_8PSK), 'o');

title(titleText);

xlabel('In-Phase');

ylabel('Quadrature');

grid on;

end
```