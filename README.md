# Scrape and Score

## Overview 
The aim of this project is to detect when quarterback passing yard projections on prop bet markets are overfit to recent game data. Bayesian analysis is used to determine whether recent game data justifies projections significantly lower, or higher than a quarterback's career average, or if public sentiment has led to innacurately priced lines. 

## Table of Contents
-[Overview](#overview)

-[Project Structure](#project-structure)

-[Data](#data)

-[Src](#src)

## Project Structure

├── data            

├── notebooks       

├── src             

├── tests           

└── README.md       

## Data
All data for this project is sourced from pro football reference. PFR provides easily accessible, high quality data, and would be my recomendation for anyone hoping to carry out a similar project.

## Src

The source code for this project, subdivided into three directories, data, features, and statistics. Data was where webscraping and data formatting were handled, features contains the scripts for feature engineering, and statistics is where functions for bayesian analysis were defined. 

### data

Formatting primarily consisted of handling rows were the quarterback did not play, and removing columns with irrelevant data.

### features

The main feature added to the data was an 'weighted yards' column that adjusted a quarterbacks passing yards for the strength of defense they faced

### statistics 

Basic functions were defined calculate probabilities in a given column of a dataframe, conditional on another column, i.e., 'probability Quarterback A passed for between 250 and 350 given they faced the number 1 ranked defense.'