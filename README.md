# Scrape and Score

## Overview 
The aim of this project is to detect when quarterback passing yard projections on prop bet markets are overfit to recent game data. Bayesian analysis is used to determine whether a quarterback's 2024 performance is strong enough (or weak enough) to provide evidence they have deviated from their historical averages

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

The source code for this project, subdivided into three directories, data, features, and statistics. 

### data

Scripts for webscraping, and formatting. Formatting primarily consisted of handling rows were the quarterback did not play, and removing columns with irrelevant data.

### features

The main feature added to the data was a 'weighted yards' column that adjusted a quarterbacks passing yards for the strength of defense they faced

### statistics 

Basic functions to calculate probabilities in a given column of a dataframe, conditional on another column, i.e., 'probability quarterback A passed for between 250 and 350 given they faced the number 1 ranked defense.' Also contains the bayesian model, which evaluates the statistical significance of a quarterback's 2024 performance. 