# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 14:12:45 2026

@author: benla
"""
'''ratkowsky solves for non-isothermal, baranyi solves for acclimation'''

'''Baranyi Attempt 1
going to use the same temp profile generator as the ratkowsky for parity'''
import csv
import math

def baranyi_model(filename):
    # --- Constants --- again this is all very rough numbers
    b = 0.025
    T_min = -5.0
    y_0 = math.log(100)        # Initial pop in ln(CFU)
    y_max = math.log(1e9)      # Max pop in ln(CFU)
    h_0 = 1.5                  # Physiological state (approx 1.5-2.0 for Pseudomonas)
    
    # Thresholds (converted to natural log for comparison)
    WARNING_LIMIT_LN = math.log(8.5e5)
    CRITICAL_LIMIT_LN = math.log(1e6)

    try:
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file)
            
            # Baranyi uses an adjustment function 'A' for the lag phase
            # A(t) represents the "readiness" of the cells
            A_t = h_0 
            y_t = y_0
            previous_time = 0.0

            print(f"{'Time (h)':<10} | {'Temp':<8} | {'Population':<15} | {'Status'}")
            print("-" * 60)

            for row in reader:
                time = float(row['Time (hours)'])
                temp = float(row['Temperature'])
                dt = time - previous_time

                # 1. Calculate mu_max via Ratkowsky
                mu_max = (b * (temp - T_min))**2 if temp > T_min else 0
                
                if dt > 0:
                    # 2. Baranyi Differential Logic (simplified integration)
                    # alpha_t is the lag phase adjustment (starts at 0, goes to 1)
                    alpha_t = A_t / (1 + A_t)
                    
                    # f_t is the inhibition function (stops growth at y_max)
                    f_t = 1 - math.exp(y_t - y_max)
                    
                    # Update population state
                    y_t = y_t + (mu_max * alpha_t * f_t * dt)
                    
                    # Update physiological state (A_t grows over time)
                    A_t = A_t * math.exp(mu_max * dt)

                # 3. Convert ln back to actual count
                actual_pop = math.exp(y_t)

                # 4. Determine Status
                status = "OK"
                if y_t >= CRITICAL_LIMIT_LN:
                    status = "!!! CRITICAL !!!"
                elif y_t >= WARNING_LIMIT_LN:
                    status = "! WARNING !"

                print(f"{time:<10.2f} | {temp:<8.1f} | {actual_pop:<15.0f} | {status}")
                
                if y_t >= y_max * 0.999:
                    print("\n--- MAXIMUM CARRYING CAPACITY REACHED ---")
                    break

                previous_time = time

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

# Run
file_to_read = input("Enter the CSV filename: ")
baranyi_model(file_to_read)