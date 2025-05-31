#!/usr/bin/env python3
"""
Script to add new training data to improve model performance
"""

import pandas as pd
import os
import sys

def load_current_dataset():
    """Load the current dataset"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    dataset_path = os.path.join(project_root, 'data', 'processed', 'dataset.xlsx')
    
    try:
        df = pd.read_excel(dataset_path)
        print(f"Current dataset loaded: {len(df)} samples")
        print(f"Spam: {len(df[df['aina'] == 'spam'])}, Ham: {len(df[df['aina'] == 'ham'])}")
        return df, dataset_path
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None, None

def add_new_messages():
    """Add new spam messages that the model failed to classify correctly"""
    
    # The message that failed classification and similar ones
    new_spam_messages = [
        # Original failing message (traditional healer/spiritual services)
        "Ata kusaidia mzee KImuka kusafisha nyota,mvuto, wa biashara, mali, kumludisha mke&mume, kazi,cheo nk,PG, no Q683817701, malipo baada ya mafanikio",
        
        # Similar traditional healer/spiritual spam messages
        "Mzee Mfalme kusaidia nyota za biashara na mali, kutoa mvuto, piga 0789123456 malipo baada ya mafanikio",
        "Daktari wa jadi kusaidia mapenzi, mali, kazi, kutoa mvuto, wasiliana 0765432198 malipo baada ya mafanikio",
        "Mzee Hassan kusaidia nyota za mali na biashara, kurudisha mke/mume, piga 0712345678",
        "Kusaidia kusafisha mvuto wa biashara na mali, kutoa uchawi, wasiliana 0723456789 malipo baada ya mafanikio",
        "Mzee Juma daktari wa jadi, kusaidia nyota za mali, mapenzi, kazi, piga 0734567890",
        "Tiba ya jadi kusaidia biashara, mali, mapenzi, kutoa mvuto, wasiliana 0745678901 malipo baada ya mafanikio",
        "Mzee Mwalimu kusaidia nyota za kazi na cheo, kurudisha mpenzi, piga 0756789012",
        "Daktari wa asili kusaidia mali na biashara, kutoa uchawi, wasiliana 0767890123 malipo baada ya mafanikio",
        "Kusaidia kusafisha nyota za maisha, biashara, mali, piga mzee Bakari 0778901234",
        
        # Mixed content with phone numbers and "malipo baada ya mafanikio"
        "Mzee wa tiba ya asili kusaidia mvuto wa mali, mapenzi, kazi, piga 0789012345 malipo baada ya mafanikio",
        "Kusaidia nyota za biashara na mali, kurudisha mke au mume, wasiliana 0790123456",
        "Daktari wa jadi Mzee Hamisi kusaidia mali, mapenzi, cheo, piga 0701234567 malipo baada ya mafanikio",
        "Tiba ya kisasa na ya jadi kusaidia biashara, mali, kutoa mvuto, wasiliana 0712345698",
        "Mzee Mwema kusaidia nyota za kazi, mali, mapenzi, kutoa uchawi, piga 0723456780"
    ]
    
    # Add some legitimate messages about traditional medicine (ham) for balance
    new_ham_messages = [
        "Daktari ameagiza dawa za jadi za sukari, nitakuja kuchukua kesho",
        "Mama amesema tukutane kwa mzee wa tiba ya asili kesho",
        "Je kuna dawa za asili za maumivu ya kichwa?",
        "Mzee wa tiba ya jadi yupo nyumbani leo?",
        "Nitahitaji dawa za jadi za kukohoa, je zipo?"
    ]
    
    return new_spam_messages, new_ham_messages

def update_dataset(df, dataset_path, new_spam_messages, new_ham_messages):
    """Add new messages to the dataset"""
    
    # Create new data
    spam_data = pd.DataFrame({
        'aina': ['spam'] * len(new_spam_messages),
        'ujumbe': new_spam_messages
    })
    
    ham_data = pd.DataFrame({
        'aina': ['ham'] * len(new_ham_messages),
        'ujumbe': new_ham_messages
    })
    
    # Combine with existing data
    updated_df = pd.concat([df, spam_data, ham_data], ignore_index=True)
    
    # Save updated dataset
    updated_df.to_excel(dataset_path, index=False)
    print(f"✅ Dataset updated and saved to: {dataset_path}")
    
    print(f"Dataset updated!")
    print(f"Added {len(new_spam_messages)} spam messages")
    print(f"Added {len(new_ham_messages)} ham messages")
    print(f"New dataset size: {len(updated_df)} samples")
    print(f"New distribution - Spam: {len(updated_df[updated_df['aina'] == 'spam'])}, Ham: {len(updated_df[updated_df['aina'] == 'ham'])}")
    
    return updated_df

def main():
    print("="*50)
    print("ADDING NEW TRAINING DATA")
    print("="*50)
    
    # Load current dataset
    df, dataset_path = load_current_dataset()
    if df is None:
        return
    
    # Get new messages
    new_spam_messages, new_ham_messages = add_new_messages()
    
    print(f"\nPreparing to add:")
    print(f"- {len(new_spam_messages)} spam messages (traditional healer type)")
    print(f"- {len(new_ham_messages)} legitimate messages")
    
    # Show some examples
    print("\nExample new spam messages:")
    for i, msg in enumerate(new_spam_messages[:3], 1):
        print(f"{i}. {msg[:80]}...")
    
    # Ask for confirmation
    response = input("\nProceed with adding these messages? (y/n): ").strip().lower()
    if response != 'y':
        print("Operation cancelled.")
        return
    
    # Update dataset
    updated_df = update_dataset(df, dataset_path, new_spam_messages, new_ham_messages)
    
    print("\n" + "="*50)
    print("DATASET UPDATED SUCCESSFULLY!")
    print("="*50)
    print("Next steps:")
    print("1. Run 'python export_model.py' to retrain with new data")
    print("2. Test the improved model with 'python use_model.py'")
    print("3. Check if the failing message is now classified correctly")

if __name__ == "__main__":
    main() 