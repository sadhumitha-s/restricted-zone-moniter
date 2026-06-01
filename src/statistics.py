import pandas as pd
import os

class SummaryStatistics:
    def __init__(self, log_file="logs/intrusion_log.csv"):
        self.log_file = log_file

    def generate_summary(self):
        """
        Reads the intrusion log and prints summary statistics.
        """
        if not os.path.exists(self.log_file):
            print(f"No log file found at {self.log_file}. Cannot generate statistics.")
            return

        try:
            df = pd.read_csv(self.log_file)
        except Exception as e:
            print(f"Error reading log file for statistics: {e}")
            return

        if df.empty:
            print("No intrusions recorded in the current log.")
            return

        print("\n=== Intrusion Summary Statistics ===")
        
        total_intrusions = len(df)
        print(f"Total Intrusions: {total_intrusions}")

        # Object Type breakdown
        if 'Object Type' in df.columns:
            print("\nBreakdown by Object Type:")
            type_counts = df['Object Type'].value_counts()
            for obj_type, count in type_counts.items():
                print(f"  {obj_type}: {count}")

        # Movement Status breakdown
        if 'Movement Status' in df.columns:
            print("\nBreakdown by Movement Status:")
            status_counts = df['Movement Status'].value_counts()
            for status, count in status_counts.items():
                print(f"  {status}: {count}")

        # Average Duration
        if 'Duration' in df.columns:
            avg_duration = df['Duration'].mean()
            print(f"\nAverage Intrusion Duration: {avg_duration:.2f} seconds")
            
        print("====================================\n")
