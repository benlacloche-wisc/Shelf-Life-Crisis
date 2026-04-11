# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 11:20:05 2026

@author: benla
"""

import csv
import math
import matplotlib.pyplot as plt

def run_calibrated_baranyi(filename):
    # --- CALIBRATED PARAMETERS ---
    # b = 0.0378 (Calibrated to match ComBase Pseudomonas at 3°C)
    b = 0.01903
    T_min = -12.9
    
    # Baranyi Constants
    y_0 = math.log(100)        # Initial pop (10^2)
    y_max = math.log(1e9)      # Max pop (Carrying capacity)
    h_0 = 1.6                  # Physiological debt
    
    # LED Thresholds
    WARN_LN = math.log(8.5e5)
    CRIT_LN = math.log(1e6)

    # Data containers for plotting
    times, temps, populations = [], [], []

    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            
            y_t = y_0
            # INITIALIZATION FOR SHARP 'J' SHAPE
            # This follows the differential form to keep lag flat until the 'snap'
            A_state = 1 / (math.exp(h_0) - 1)
            
            prev_time = 0.0

            print(f"{'Time':<8} | {'Temp':<6} | {'Pop (CFU)':<12} | {'LED Status'}")
            print("-" * 50)

            for row in reader:
                t = float(row['Time (hours)'])
                temp = float(row['Temperature'])
                dt = t - prev_time

                if dt > 0:
                    # 1. Update growth rate (Ratkowsky)
                    mu_max = (b * (temp - T_min))**2 if temp > T_min else 0
                    
                    # 2. Baranyi Adjustment (The Sharp J Logic)
                    alpha_t = A_state / (1 + A_state)
                    f_t = 1 - math.exp(y_t - y_max)
                    
                    # 3. Stepwise Integration
                    y_t += (mu_max * alpha_t * f_t * dt)
                    
                    # 4. Update internal state (Waking up the bacteria)
                    A_state += (mu_max * A_state * dt)

                pop_actual = math.exp(y_t)
                
                # LED Logic
                if y_t >= CRIT_LN:
                    status = "RED"
                elif y_t >= WARN_LN:
                    status = "YELLOW"
                else:
                    status = "GREEN"

                # Store for graphing
                times.append(t)
                temps.append(temp)
                populations.append(pop_actual)

                print(f"{t:<8.2f} | {temp:<6.1f} | {int(pop_actual):<12} | {status}")
                prev_time = t

        # --- GRAPHING SECTION ---
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Population Plot
        ax1.set_xlabel('Time (hours)')
        ax1.set_ylabel('Population (CFU/g)', color='tab:blue')
        ax1.plot(times, populations, color='tab:blue', linewidth=3, label='Pseudomonas (Baranyi)')
        ax1.set_yscale('log')
        ax1.tick_params(axis='y', labelcolor='tab:blue')

        # Threshold Lines
        ax1.axhline(y=8.5e5, color='orange', linestyle='--', alpha=0.6, label='Warning Threshold')
        ax1.axhline(y=1e6, color='red', linestyle='--', alpha=0.6, label='Spoilage Threshold')

        # Temp Plot
        ax2 = ax1.twinx()
        ax2.set_ylabel('Temperature (°C)', color='tab:red')
        ax2.plot(times, temps, color='tab:red', linestyle=':', alpha=0.5, label='Temp Profile')
        ax2.tick_params(axis='y', labelcolor='tab:red')

        plt.title('Calibrated Sharp-J Growth Model (Milk Spoilage)')
        fig.tight_layout()
        ax1.legend(loc='upper left')
        
        plt.show()

    except FileNotFoundError:
        print("CSV file not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Run
file_to_analyze = input("Enter the CSV filename: ")
run_calibrated_baranyi(file_to_analyze)
