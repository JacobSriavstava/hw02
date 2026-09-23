Create one single python script that does the following steps all within one single run:
1. Load the fact_transactions.csv data file into a pandas DataFrame. This file can be found in the raw folder within the data folder.
2. Print the shape (rows X columns)
3. Print all column names and their data types
4. Print the count of missing values for every column
5. Print descriptive statistics (Count, mean, standard deviation, min, 25th percentile, median, 75th percentile, and max) for all numeric columns
6. Print value counts and percentages for txn_type, sort from most to least frequent
7. Print the unique count of clients, advisors, and securities referenced in the file
8. Print the earliest and latest txn_date (the date range of the dataset)
9. Check for duplicate rows by txn_id and print the duplicate count
10. Print the mean, median, and skewness of the amount column
11. Group the data by txn_type and prints, for each type, the count and the mean and median amount (rounded to 2 decimal places), sorted by mean amount decending
12. Compute the correlation matrix for shares, prices, and amount (Round to 2 decimal places), print it, and identifie the three strongest correlations (excluding a variable's correlation with itself)
13. Print the minimum, maximum, and count of negative values in the shares column, broken out by txn_type.
14. Print a warning if the shape is not(298772,0)
15. Create and save three charts to the hw02/charts folder: a histogram of amount with vertical lines and the mean and median, labled clearly (hw02/charts/hist_amount.png); and a scatter plot of shares (x-axis) vs. amount (y-axis) colored by txn_type (hw/02/charts/scatter_shares_amount.png)
16. Save a plain-text summary of items 2-13 to hw02/hw02_profile.txt
17. Include a comment block at the top identifying the script, dataset, author, and generation date.

18. This is one script. Not 17 different separate scripts. All items must run together in the same file, in one execution. 