#!/usr/bin/env python3

import argparse

def parse_log_file(filename):
    process_times = {}
    
    with open(filename, 'r') as f:
        for line in f:
            if 'PID-' not in line:
                continue
            
            parts = line.strip().split(',')
            if len(parts) < 3:
                continue
            
            pid_part = parts[1].strip()
            time_part = parts[2].strip()
            try:
                pid = int(pid_part.split('-')[1])
            except (IndexError, ValueError):
                continue
            
            try:
                time = float(time_part.rstrip('s'))
                if pid not in process_times:
                    process_times[pid] = 0.0
                process_times[pid] += time
            except ValueError:
                continue
    
    return process_times

def calculate_percentage(process_times, target_pid):
    total_time = sum(process_times.values())
    if total_time == 0:
        return 0.0
    
    process_percentage = (process_times[target_pid] / total_time) * 100
    return process_percentage

def main():
    parser = argparse.ArgumentParser(description='Process log file and calculate processor time percentage')
    parser.add_argument('-p', '--process', type=int, default=2, help='Process number to analyze (default: 2)')
    parser.add_argument('-f', '--file', type=str, default='system.log', help='Log file to analyze (default: system.log)')
    args = parser.parse_args()
    
    try:
        process_times = parse_log_file(args.file)
        if args.process not in process_times or process_times[args.process] == 0.0:
            print(f"Error: PID-{args.process} not found in the log file.")
            return
        percentage = calculate_percentage(process_times, args.process)
        print(f"PID-{args.process} consumed {percentage:.2f}% of the processor time")
    except FileNotFoundError:
        print(f"Error: {args.file} file not found")
    except Exception as e:
        print(f"Error processing log file: {str(e)}")

if __name__ == "__main__":
    main()
