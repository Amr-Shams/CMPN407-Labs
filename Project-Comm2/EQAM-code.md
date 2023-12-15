```c
clear;

%% --- QAM Modulation and Demodulation Simulation ---

% Parameters

N_QAM = 48000; % Number of bits

Eb_QAM = 2.5; % Energy of bit

no_of_bits_in_symbol_QAM = 4; % Number of bits in symbol

symbols_number_QAM = 16; % Number of symbols in QAM

% Generate random bits

random_bits_binary_QAM = randi([0, 1], 1, N_QAM);

% Map bits to symbols for QAM

mapped_QAM = QAM_modulate(random_bits_binary_QAM, no_of_bits_in_symbol_QAM, symbols_number_QAM);

% Plot some random samples before transmission

figure('Name', 'QAM Modulation: Random Samples Before Transmission');

plot(real(mapped_QAM), imag(mapped_QAM), 'o');

title('QAM Modulation: Random Samples Before Transmission');

xlabel('Real Part');

ylabel('Imaginary Part');

grid on;

%% --- Channel Noise ---

SNR_QAM = 1:10;

BER_QAM = zeros(1, length(SNR_QAM));

for i = 1:length(SNR_QAM)

No_QAM = Eb_QAM / 10^(SNR_QAM(i) / 10);

% Add noise to the signal

noise_with_unity_variance_QAM = randn(1, length(mapped_QAM)) + 1j * randn(1, length(mapped_QAM));

signal_QAM_after_channel = mapped_QAM + noise_with_unity_variance_QAM * sqrt(No_QAM / 2);

% Demap symbols to bits for QAM

demapped_QAM = QAM_demodulate(signal_QAM_after_channel, symbols_number_QAM);

% Bit error for each filter

number_of_bit_errors_QAM = random_bits_binary_QAM - demapped_QAM;

% Calculate Bit Error Rate

BER_QAM(i) = sum(abs(number_of_bit_errors_QAM)) / N_QAM;

end

% Plot some random samples after transmission

figure('Name', sprintf('QAM Demodulation: Random Samples After Transmission (SNR = %ddB)', SNR_QAM(9)));

plot(real(signal_QAM_after_channel), imag(signal_QAM_after_channel), 'o');

title(sprintf('QAM Demodulation: Random Samples After Transmission (SNR = %ddB)', SNR_QAM(9)));

xlabel('Real Part');

ylabel('Imaginary Part');

grid on;

% Theoretical BER of QAM

theoretical_BER_QAM = 1.5 / 4 * erfc((sqrt(10.^(SNR_QAM / 10))) * sqrt(1 / 2.5));

% Plotting

figure('Name', 'BER vs Eb/N0 for QAM');

semilogy(SNR_QAM, BER_QAM, 'r');

hold on;

semilogy(SNR_QAM, theoretical_BER_QAM, 'Color', 'k', 'LineStyle', '--');

xlabel('SNR = Eb/No (dB)');

ylabel('BER');

grid on;

title('BER vs Eb/N0 for QAM');

legend('QAM BER', 'Theoretical QAM BER');

function mapped_symbols = QAM_modulate(bits, no_of_bits_in_symbol, symbols_number)

% QAM Modulation function

% bits: Input binary bit stream

% no_of_bits_in_symbol: Number of bits in each symbol

% symbols_number: Number of symbols in the QAM modulation

% Define the mapping for QAM symbols

mapped_bits_QAM = [

0 0 0 0; 0 0 0 1; 0 0 1 1; 0 0 1 0;

0 1 0 0; 0 1 0 1; 0 1 1 1; 0 1 1 0;

1 1 0 0; 1 1 0 1; 1 1 1 1; 1 1 1 0;

1 0 0 0; 1 0 0 1; 1 0 1 1; 1 0 1 0

];

A = 1;

% Symbols represented in QAM

mapped_symbols_QAM = [

A * (-3 - 3j) A * (-3 - 1j) A * (-3 + 1j) A * (-3 + 3j);

A * (-1 - 3j) A * (-1 - 1j) A * (-1 + 1j) A * (-1 + 3j);

A * (1 - 3j) A * (1 - 1j) A * (1 + 1j) A * (1 + 3j);

A * (3 - 3j) A * (3 - 1j) A * (3 + 1j) A * (3 + 3j)

];

% Initialize mapped symbols array

mapped_symbols = zeros(1, length(bits) / no_of_bits_in_symbol);

% Map bits to symbols

counter = 1;

for i = 1:no_of_bits_in_symbol:length(bits)

for count = 1:symbols_number

if isequal(bits(i:i + no_of_bits_in_symbol - 1), mapped_bits_QAM(count, :))

mapped_symbols(counter) = mapped_symbols_QAM(count);

end

end

counter = counter + 1;

end

end

function demapped_bits = QAM_demodulate(signal, symbols_number)

% QAM Demodulation function

% signal: Input signal after channel

% symbols_number: Number of symbols in the QAM modulation

% Define the mapping for QAM symbols

mapped_bits_QAM = [

0 0 0 0; 0 0 0 1; 0 0 1 1; 0 0 1 0;

0 1 0 0; 0 1 0 1; 0 1 1 1; 0 1 1 0;

1 1 0 0; 1 1 0 1; 1 1 1 1; 1 1 1 0;

1 0 0 0; 1 0 0 1; 1 0 1 1; 1 0 1 0

];

A = 1;

% Symbols represented in QAM

mapped_symbols_QAM = [

A * (-3 - 3j) A * (-3 - 1j) A * (-3 + 1j) A * (-3 + 3j);

A * (-1 - 3j) A * (-1 - 1j) A * (-1 + 1j) A * (-1 + 3j);

A * (1 - 3j) A * (1 - 1j) A * (1 + 1j) A * (1 + 3j);

A * (3 - 3j) A * (3 - 1j) A * (3 + 1j) A * (3 + 3j)

];

% Initialize demapped bits array

demapped_bits = zeros(1, length(signal) * 4);

% Demap symbols to bits

counter = 1;

for j = 1:length(signal)

% Array to store distance

array_of_distances_QAM = zeros(1, symbols_number);

% Loop to get distance of received symbol with all the constellation points

for count = 1:symbols_number

array_of_distances_QAM(count) = abs(signal(j) - mapped_symbols_QAM(count));

end

% Get minimum distance

min_distance_QAM = min(array_of_distances_QAM);

for count = 1:symbols_number

if array_of_distances_QAM(count) == min_distance_QAM

demapped_bits(counter:counter + 3) = mapped_bits_QAM(count, :);

end

end

counter = counter + 4;

end

end

function saveAllFigures()

figHandles = findall(0, 'Type', 'figure');

for i = 1:length(figHandles)

figure(figHandles(i));

saveFigure(['Figure_' num2str(i)]);

end

end
```