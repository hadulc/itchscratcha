import os
import pandas as pd
import glob
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("merge.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("fighter_data_merger")

def merge_csv_files() -> pd.DataFrame:
    """
    Merge all CSV files from the data directory into a single DataFrame.
    
    Returns:
        pd.DataFrame: Combined DataFrame with all fighter data
    """
    logger.info("Starting to merge CSV files from data directory")
    
    # Get all CSV files in the data directory
    csv_files = glob.glob("data/fighter_rankings_*.csv")
    
    if not csv_files:
        logger.warning("No CSV files found in the data directory")
        return pd.DataFrame()
    
    logger.info(f"Found {len(csv_files)} CSV files to merge")
    
    # Create an empty list to store individual DataFrames
    dfs = []
    
    # Track progress
    total_files = len(csv_files)
    processed = 0
    
    # Read each CSV file and append to the list
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            if not df.empty:
                dfs.append(df)
            processed += 1
            
            # Log progress periodically
            if processed % 100 == 0 or processed == total_files:
                logger.info(f"Processed {processed}/{total_files} files")
                
        except Exception as e:
            logger.error(f"Error reading file {file}: {str(e)}")
    
    # Combine all DataFrames
    if dfs:
        combined_df = pd.concat(dfs, ignore_index=True)
        logger.info(f"Successfully merged {len(dfs)} files into a DataFrame with {len(combined_df)} rows")
        return combined_df
    else:
        logger.warning("No valid data found in CSV files")
        return pd.DataFrame()

if __name__ == "__main__":
    # Merge all CSV files
    merged_data = merge_csv_files()
    
    if not merged_data.empty:
        # Save the merged data to a new CSV file
        output_file = "merged_fighter_data.csv"
        merged_data.to_csv(output_file, index=False)
        logger.info(f"Merged data saved to {output_file}")
        
        # Display some statistics
        logger.info(f"Total records: {len(merged_data)}")
        logger.info(f"Unique fighters: {merged_data['name'].nunique()}")
        logger.info(f"Unique issues: {merged_data['issue'].nunique()}")
        logger.info(f"Unique divisions: {merged_data['division'].nunique()}")
    else:
        logger.error("Failed to create merged dataset")
