# 1.Introduction

The ever-evolving landscape of communication systems demands continuous exploration and experimentation to enhance the efficiency and reliability of data transmission. This project delves into the intricacies of modulation and demodulation schemes, specifically focusing on Binary Phase Shift Keying (BPSK), Quadrature Phase Shift Keying (QPSK), 8-Phase Shift Keying (8PSK), and 16-Quadrature Amplitude Modulation (16QAM). These modulation techniques play a pivotal role in shaping the communication protocols that facilitate the transfer of information over various channels.

The primary objective of this project is to investigate and analyze the performance of different modulation schemes in the presence of additive white Gaussian noise (AWGN). We explore the mapping of input data bits to symbols, simulate the transmission through a noisy channel, and subsequently demap the received symbols to estimate the Bit Error Rate (BER). Through MATLAB implementations, we gain insights into the robustness and reliability of each modulation scheme under varying signal-to-noise ratio (SNR) conditions.

This exploration is facilitated by a systematic experimental setup, encompassing the mapper, channel, and demapper components. The choice of an AWGN channel introduces a realistic and widely used model for analyzing communication systems. By employing MATLAB functionalities such as "randn" for generating AWGN, we emulate real-world conditions and evaluate the impact of noise on the performance of modulation schemes.

The project unfolds with an overview of the experimental setup, providing a comprehensive understanding of the mapper, channel, and demapper components. Each modulation scheme is discussed individually, highlighting the key aspects of its design and implementation. The impact of AWGN on the transmission process is scrutinized, and the demapping process is elucidated to calculate the BER.

Through detailed experimental results and visualizations, we aim to provide a nuanced perspective on the strengths and limitations of each modulation scheme, thereby contributing valuable insights to the field of communication systems. The project's findings not only serve as a benchmark for understanding the behavior of modulation schemes but also pave the way for future enhancements and optimizations in communication protocols.

# 2.Experimental Setup

## 2.1 Mapper

The Mapper is a fundamental component in the communication system, responsible for translating input data bits into symbols that are suitable for transmission over a channel. In the context of this project, we specifically examine four modulation schemes: Binary Phase Shift Keying (BPSK), Quadrature Phase Shift Keying (QPSK), 8-Phase Shift Keying (8PSK), and 16-Quadrature Amplitude Modulation (16QAM). Each of these schemes employs a unique mapping strategy to represent a group of bits with a corresponding symbol.

- **BPSK Mapper:** In BPSK, each bit is mapped to a phase shift of 0 or 180 degrees, resulting in two distinct symbols. This straightforward mapping allows for a simple and robust transmission of binary data.

- **QPSK Mapper:** QPSK extends BPSK by mapping pairs of bits to specific phases, introducing four distinct symbols. This enables the transmission of two bits per symbol, effectively doubling the data rate compared to BPSK.

- **8PSK Mapper:** Moving further, 8PSK maps groups of three bits to eight different phases. This scheme increases the data rate per symbol but requires careful consideration of phase transitions to mitigate errors.

- **16QAM Mapper:** In 16QAM, each symbol represents a combination of four bits, utilizing both amplitude and phase modulation. This allows for an even higher data rate but requires a more sophisticated mapping strategy.

## 2.2 Channel

The Channel represents the medium through which the modulated symbols traverse. In this project, we model the channel as an Additive White Gaussian Noise (AWGN) channel. The AWGN channel introduces random noise to the transmitted signal, simulating real-world interference and environmental conditions. The `randn` function in MATLAB is employed to generate random noise samples with a Gaussian distribution, reflecting the inherent unpredictability of practical communication channels.

2.3 Demapper

The Demapper is the counterpart to the Mapper and plays a crucial role in the receiver's signal processing. It is tasked with interpreting the received symbols, often in the presence of noise, and determining the corresponding bits. In the context of this project, the Demapper analyzes the received signal and compares it to the predefined constellation points of each modulation scheme. By calculating distances or using other decision metrics, the Demapper decodes the symbols and outputs an estimated bit sequence. The Bit Error Rate (BER) is then computed by comparing the estimated bits to the original transmitted bits, providing insights into the accuracy of the communication system under varying channel conditions.

# 3.Modulation Schemes Overview

## 1. BPSK (Binary Phase Shift Keying)

BPSK is a basic modulation scheme where binary data is represented by two phase states of the carrier signal (0 and 180 degrees). It is known for its simplicity and resilience to noise.

2. QPSK (Quadrature Phase Shift Keying)

QPSK extends BPSK by encoding two bits per symbol, using four distinct phase shifts. This enhances data rate and spectral efficiency but increases susceptibility to phase errors.

## 3. 8PSK (8-Phase Shift Keying)

8PSK further increases data rate by encoding three bits per symbol, employing eight phase shifts. While offering higher efficiency, it becomes more sensitive to phase variations.

## 4. 16QAM (16-Quadrature Amplitude Modulation)

16QAM combines phase and amplitude modulation, representing four bits per symbol. It utilizes a 4x4 grid of constellation points, providing a higher data rate at the cost of increased susceptibility to noise.

# 4. MATLAB Code

The following code is what we used for each type.
BPSK
[[BSK-code]] 
![[Pasted image 20231217012200.png]]
![[Pasted image 20231217012216.png]]

### 1. BPSK (Binary Phase Shift Keying) Modulation

#### 1.1. `main` Function

- This function serves as the entry point for the BPSK modulation simulation.
- It generates random bits, creates a BPSK signal, adds noise, and evaluates the Bit Error Rate (BER).

#### 1.2. `generateBits` Function

- Generates a random sequence of binary bits.

#### 1.3. `generateSignal` Function

- Generates the BPSK signal by mapping bits to phase shifts (0 or 180 degrees).
- Plots the generated signal.

#### 1.4. `generateBPSKSignal` Function

- Generates the BPSK modulated signal based on the mapping of bits to phase shifts.

#### 1.5. `simulateBPSKModulation` Function

- Simulates BPSK modulation with additive white Gaussian noise (AWGN).
- Calculates and plots the Bit Error Rate (BER) for different Signal-to-Noise Ratio (SNR) levels.

#### 1.6. `simulateBPSKModulationWithAWGN` Function

- Simulates BPSK modulation with AWGN and calculates the BER.
- Compares the received bits with the original bits for error calculation.
--------------------

QPSK
[[QPSK-code]]

![[Pasted image 20231217012434.png]]
![[Pasted image 20231217012452.png]]
![[Pasted image 20231217012504.png]]

### 2. QPSK (Quadrature Phase Shift Keying) Modulation

#### 2.1. `main` Function

- Similar to BPSK, this function is the entry point for the QPSK modulation simulation.

#### 2.2. `QPSK Modulation and Demodulation`

- QPSK modulation involves encoding two bits per symbol using four distinct phase shifts.
- QPSK demodulation involves coherent detection using in-phase and quadrature components.

#### 2.3. `simulateQPSKModulation` Function

- Simulates QPSK modulation with AWGN.
- Plots the BER curve for different SNR levels.

------------

EPSK or 8PSK

[[EPSK-code]]

![[Pasted image 20231217012809.png]]
![[Pasted image 20231217012826.png]]
![[Pasted image 20231217012847.png]]

### 3. 8PSK (8-Phase Shift Keying) Modulation

#### 3.1. `clear` and `close all`

- Clears variables and closes existing figures.

#### 3.2. `main` Function

- Entry point for the 8PSK modulation simulation.

#### 3.3. `QAM_modulate` Function

- Maps binary bits to symbols for 8PSK modulation.
- Defines the constellation points and maps bits to corresponding symbols.

#### 3.4. `QAM_demodulate` Function

- Demaps symbols to bits for 8PSK demodulation.
- Calculates distances between received symbols and constellation points.

#### 3.5. `plotConstellation8PSK` Function

- Plots the constellation diagram for 8PSK modulation.

#### 3.6. `saveAllFigures` Function

- Saves all generated figures.
----------
EQAM
[[EQAM-code]]

![[Pasted image 20231217013622.png]]
![[Pasted image 20231217013642.png]]
![[Pasted image 20231217013657.png]]

### 4. QAM (Quadrature Amplitude Modulation) Modulation

#### 4.1. `clear`

- Clears existing variables.

#### 4.2. `main` Function

- Entry point for the QAM modulation simulation.

#### 4.3. `QAM_modulate` and `QAM_demodulate` Functions

- Similar to those used in 8PSK, these functions handle mapping and demapping for QAM modulation.

#### 4.4. `saveAllFigures` Function

- Saves all generated figures.