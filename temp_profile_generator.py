# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 09:01:34 2026

@author: benla
"""
import csv
import random
import os

def simulate_and_save():
    print(f"File will be saved in: {os.getcwd()}")
    
    try:
        # 1. Configuration Inputs
        count = int(input("How many measurements? "))
        increment = float(input("Time increment (hrs)? "))
        start_temp = float(input("Base temperature? "))
        
        print("\nTemperature Behavior:")
        print("1. Static (constant temperature)")
        print("2. Drift (randomly fluctuates)")
        mode = input("Select 1 or 2: ")
        
        filename = input("Enter filename to save (e.g., data.csv): ")
        if not filename.endswith('.csv'):
            filename += '.csv'

        # 2. Generate and Write
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Time (hours)", "Temperature"])

            current_temp = start_temp
            
            for i in range(count):
                timestamp = round(i * increment, 2)
                
                if mode == '2':
                    # Add drift only if mode 2 is selected
                    current_temp += random.uniform(-0.4, 0.4)
                else:
                    # In static mode, we keep it exactly at start_temp
                    current_temp = start_temp
                
                writer.writerow([timestamp, round(current_temp, 2)])

        print(f"\nSuccess! '{filename}' created with {count} readings.")

    except ValueError:
        print("Error: Please enter numbers for the settings.")

if __name__ == "__main__":
    simulate_and_save()