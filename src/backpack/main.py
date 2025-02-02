#!/usr/bin/env python3

import os
import pandas as pd
import numpy as np
import pickle
from dotmap import DotMap
from datetime import datetime
    
class Backpack:
    ''' Backpack database containing all data corresponding to a (biased) MD run. '''

    def __init__(self, location=f"{os.getcwd()}/backpack.pkl", verbose=True):
        ''' Initialize the database ''' 
        self.verbose = verbose
        self.location = os.path.expanduser(location)

        print(f"Looking for existing backpack in {self.location}...", end="") if self.verbose else 0
        self.load(self.location)


    def load(self , location):
        ''' See if a database exists, if not, create a new database. '''
        if os.path.exists(location):
            self._load()
            print(f"done") if self.verbose else 0
            print(f"Backpack contains the following items:") if self.verbose else 0

            self.list() if self.verbose else 0
        else:
            print(f"not found") if self.verbose else 0
            print(f"! Warning:\tNo database was found at {location}") if self.verbose else 0
            print(f"\t\tCreating new database.") if self.verbose else 0
            self.content = {}
        return

    def _load(self):
        ''' Load database from file. '''
        with open(self.location, 'rb') as handle:
            self.content = pickle.load(handle)

    def dump(self):
        try:
            with open(self.location, 'wb') as handle:
                pickle.dump(self.content, handle, protocol=-1)

            return
        except Exception as e:
            print(f"! ERROR: Could not dump database into {self.location}") if self.verbose else 0
            print(f"\t{e}") if self.verbose else 0
            return False

    def set(self, key, value):
        
        # Set attribute
        self.content[str(key)] = value
        self.dump()
            
        return

    def get(self, key):    
        
        return self.content[key]
        
    def delete(self, key):
        if not key in self.content:
            return False
        del self.content[key]
        self.dump()
        return

    def list(self):
        print(f"   {'Key':<20}{'Type':<30}{'Content/Value':<60}Shape")

        # Get terminal size for adjusted printing
        try:
            size = os.get_terminal_size() 
            print("-" * size.columns)
        except Exception:
            print("-" * 130)
    
        for key, value in self.content.items():
            
            # If you have a dataframe, output the columns and shape of the dataframe.
            item = self.content[key]
            
            if isinstance(item, pd.DataFrame):
                # If dataframe show column names and shape.
                columns = item.columns.values
                content = f"Columns: [{', '.join(map(str, columns[:2]))}, ..., {', '.join(map(str, columns[-2:]))}]"
                shape = f"{item.shape}"
                t = "pd.Dataframe"
            elif isinstance(item, (np.ndarray, np.generic) ):
                # If numpy array show first and last two values and shape.
                content = f"np.array: [{', '.join(map(str, value[:2]))}, ..., {', '.join(map(str, value[-2:]))}]"
                shape = f"Shape: {np.shape(item)}"
                t = type(value)
            elif isinstance(item, list):
                # If numpy array show first and last two values and shape.
                content = f"list: [{', '.join(map(str, value[:2]))}, ..., {', '.join(map(str, value[-2:]))}]"
                shape = f"Shape: {np.asarray(content).shape}"
                t = type(value)
            elif isinstance(item, DotMap):
                # If numpy array show first and last two values and shape.
                content = f"DotMap: [{', '.join([k for k in value.keys() if not k.startswith('_')])}]"
                shape = f"Shape: {np.asarray(content).shape}"
                t = type(value)
            else:
                # Otherwise just output the value
                content = value

                shape = "-"
                t = type(value)

            print(f"-> {key:<20}{str(t):<30}{str(content):<60}{shape}")
        return

    def backup(self):

        # Backup database
        backpack_filename = os.path.basename(self.location)
        idx = backpack_filename.index('.')
        backup_basename = backpack_filename[:idx] + f"_backup_{datetime.today().strftime('%Y%m%d%H%M%S')}" + backpack_filename[idx:]

        backup_location = f"{os.path.dirname(self.location)}/{backup_basename}"

        try:
            with open(backup_location, 'wb') as handle:
                pickle.dump(self.content, handle, protocol=-1)
            
                print(f"Backed up backpack to {backup_location}") if self.verbose else 0

            return
        except Exception as e:
            print(f"! ERROR: Could not dump database into {backup_location}") if self.verbose else 0
            print(f"\t{e}") if self.verbose else 0
            return False