import csv
import math

def calculate_growth_with_limits(filename):
    # Ratkowsky Constants for Pseudomonas
    b = 0.025 #this is just published b, we can make our own. 
    #I will say this is drastically lower than what I calculated 
    #for the excel model, but that was back-of-napkin math so let's refine
    T_min = -5.0
    initial_population = 100.0 
    #really this whole block needs refining but that's for another day
    
    # Thresholds
    WARNING_LIMIT = 850000.0  # 8.5e5
    CRITICAL_LIMIT = 1000000.0 # 1e6
    
    try: #using files from my "temp_profile_generator" 
        with open(filename, mode='r') as file:
            reader = csv.DictReader(file) #reads headers instead of indices
            
            current_population = initial_population
            previous_time = 0.0
            
            print(f"{'Time (h)':<10} | {'Temp':<8} | {'Population':<15} | {'Status'}")
            print("-" * 55)

            for row in reader:
                time = float(row['Time (hours)'])
                temp = float(row['Temperature'])
                
                # 1. Calculate growth rate
                mu = (b * (temp - T_min))**2 if temp > T_min else 0
                
                # 2. Update population
                dt = time - previous_time
                if dt > 0:
                    current_population *= math.exp(mu * dt) #see notebook or 
                    #excel to understand this math

                # 3. Determine Status
                status = "OK"
                if current_population >= CRITICAL_LIMIT:
                    status = "!!! CRITICAL (1e6) !!!"
                elif current_population >= WARNING_LIMIT:
                    status = "! WARNING (8.5e5) !"

                # 4. Print results
                print(f"{time:<10.2f} | {temp:<8.1f} | {current_population:<15.0f} | {status}")
                
                # Optional: Stop simulation if critical limit is reached
                if current_population >= CRITICAL_LIMIT:
                    print("\n--- SPOILAGE LIMIT REACHED ---")
                    print(f"Product hit critical levels at {time} hours.")
                    break
                
                previous_time = time

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")

# Run the program
file_to_read = input("Enter the CSV filename to analyze: ")
calculate_growth_with_limits(file_to_read)