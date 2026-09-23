| Check | Expected | Your Script Produced | Match? | Notes |
|---|---|---|---|---|
| Dataset shape | (298772, 9) | 298,772 X 9| Yes| |
| Null count — `security_id` | 101,597 | 101,597 | Yes| |
| Null count — `amount` | 0 | 0 | Yes | |
| Unique `txn_type` values | 6 | 6 | Yes| |
| Count of `Buy` transactions | 83,556 |83,556 | Yes| |
| `txn_date` data type | object | str| No | I have a different version of panda so it is labeled as something different. My conversation with Claude: Why for the txt_date data type does the benchmark say object and mine says str? Claude output: That's a version difference, not a data problem. The benchmark table was built using an older version of pandas, where text columns (like txn_date and txn_type) are stored internally as generic Python objects — pandas labels that dtype object. You have pandas 3.0.6 installed (a very recent release). Starting with pandas 3.x, pandas introduced a new native string dtype for text columns, and it now displays as str instead of the legacy object label.The actual data hasn't changed — txn_date is still being read in as plain text (not parsed into a real date type), which is exactly the same underlying behavior the assignment wants you to notice and flag. Only the printed name of that dtype changed between pandas versions.  |
| Earliest `txn_date` | 2020-01-01 | 2020-01-01 | Yes| |
| Latest `txn_date` | 2024-12-30 |2024-12-30 |Yes | |
| Duplicate `txn_id` count | 0 |0 |Yes | |
| Mean `amount` | $54,075.17 | $54,075.17|Yes | |
| Median `amount` | $41,220.48 | $41,220.49 | Yes| |
| Skewness of `amount` | 1.15 | 1.15 | Yes | |
| Correlation `shares`–`amount` | 0.65 | 0.65 | Yes| |
| Correlation `price`–`amount` | 0.64 | 0.64| Yes| |
| Correlation `shares`–`price` | 0.00 | 0.00 | Yes| |
| Negative `shares` count (Buy only) | 836 | 836| Yes | |
| Profile file created | Yes | Yes, a profile file was created| Yes| |
| Chart files created (3) | Yes | Yes, three charts were created | Yes| |

## Part 2B - Explain the Code and the Output
---

1. Did Claude's Predicted outputs (From Propt 1) match what you actually saw in the terminal? List any discrepencies

Yes, Claudes predicted outputs were the exact same as the one in my terminal. The only difference was with the object and str but when I asked Claude what teh difference was it was because there was a different version of Panda used and they meant the same thing.

2. What did Claude flag as potentially unexpected or worth investigating (From Prompt 2)

a. The divident amount looked wrong
b. 836 buy rows have negative shares. Their amount is still positive. It must either be a data-entry error or they are cancelled or reversed trades.
c. Every amount is positive, including withdrawls, advisory fees, and sells.
d. Advisory feels look too high
e. 28% of transactions fall on weekends. The markets are closed then, so weekend buy, sell, and dividents are not realistic. Deposits could be.
f. Sells exceed holdings
g. Some clients IDs never appear
h. Share counts and prices are unnaturally even
i. Transaction volume changes by year

3. Did Claude mention the 101,597 null values in security_id? What explanation did it give?

Yes, it did. The explaination was that they are all deposit, withdrawl, and advisoty fee rows, which have no security involved. The blanks are expected

4. Did Claude flag the txt_date column as a concern? Why would that matter for a time-series analysis?

If flagged it as a data type. It says they show str because pythones project setup under a newer panda label text column. It is harmless. Security_id is stored as a decimal number only because it has blanks. 

5. Open your three chart files. Does what you see in each image match CLaude's explanation of that section of the output? Note any differences

Yes, they do. The numbers line up. The only one I had a hard time comparing is the scatter_shares_amount.png as I was confused by the description and on how to interpret the graph.

6. Paste one follow-up question you asked CLaude, and Claudes Answer

My follow up question: How would you integrate the volume changes by year into a report to make the analytics the most effective?

Claude Response: The main thing I'd do is split total volume into its drivers instead of reporting the raw count by itself. I computed the numbers from your data, and they show the drivers aren't all moving the same way:

Year	Transactions	Active clients	New clients	Txns per client	Median txn	YoY txns
2020	41,949	1,865	1,865*	22.5	$41,079	—
2021	51,277	2,190	348	23.4	$41,350	+22.2%
2022	65,083	2,547	400	25.6	$40,944	+26.9%
2023	73,058	2,548	51	28.7	$41,214	+12.3%
2024	67,405	2,361	36	28.5	$41,537	−7.7%

*2020 is the first year of data, so every client looks "new" that year.

What this shows:

2020–2022: growth came mostly from adding clients.
2022–2023: growth came from more activity per client, since the client count stayed flat.
2024: the drop comes from losing about 190 active clients while bringing in only 36 new ones. Activity per client held steady.
Constant: the median transaction size ($41K) and the mix of transaction types (Buy ~28%, Sell ~20%, and so on) barely changed across the five years.

The raw count alone just reads "grew, then dipped." Broken down, the story is that client acquisition stalled after 2022 and retention slipped in 2024, which gives a manager something to act on.

How I'd build it into the report
Open with the breakdown, not the total. Use one small-multiples chart: four side-by-side panels (transactions, active clients, txns per client, median size), each showing 2020 = 100. That way readers see which driver moved and which stayed flat.
Divide by active clients wherever you compare years. Show dollar amounts per client and transaction counts per client next to any yearly total, so growth in the client base doesn't look like better performance.
Add a client-flow bridge for each year: clients at the start of the year, plus new clients, minus clients who stopped transacting, equals clients at year-end. This is where the 2024 story shows up most clearly.
Use medians and mix percentages for anything that isn't a volume measure. Because they're stable, they show readers that behavior didn't change even though volume did.
Use monthly data for trends and keep yearly figures for headline numbers. Monthly volume went from about 3,200 (Jan 2020) to about 5,600 (late 2024). A monthly line, or a rolling 12-month line, shows exactly when the peak happened in 2023 or 2024.
Add a data-notes box. It should say that 2020 has no earlier year to compare against, that amounts aren't signed and Dividend amounts are inflated (so dollar totals like the ~$3.7B for 2024 aren't reliable yet), and that the data looks synthetic.
KPI tiles

If you're making a dashboard (Power BI would work well for this), I'd use these four tiles, each showing year-over-year change:

Active clients: 2,361, down 7.3%.
New clients: 36, the lowest in the five years.
Transactions per client: 28.5, flat.
Median transaction: $41.5K, flat.


## Part 2C - Business Check & Cross-Validation

1. security_id, shares, and price are all null in exactly 101,597 rows. Looking at the txn_type value counts, which three transaction types would you expect to have no security — and why? Does the counts add up to 101,597?

Deposits, withdrawls, and advisory fees because they are cash movements. Not trades. Yes, they add up exactly to 101,597.

2. There are 83,556 Buy transactions and 59,755 Sell transactions. What does it mean for a wealth management firm to have significantly more Buys than Sells over a five-year period?

This means there are about 23,800 more buys than sells. This means that clients purchase investments more often than they sell them. It could also mean clients are adding money to their porfolio overtime.

3. The txn_date column is stored as a string (type object) rather than a date. If Claude Cowork generated code to compute the average number of days between transactions, what would go wrong if the dates remained as strings?

Subtracting two strings does not work and would result in wrong data and wrong answers. This would be a big problem as the analysis would be off. 

4. Wildcat Capital has 2,700 clients served by 25 advisors. Is that ratio — roughly 108 clients per advisor — plausible for a registered investment advisory firm?

Yes, this is plausible for a registered investment advisoty firm. However, the advisors need to be of high level as 108 clients is a significant number for one advisor. 

5. 836 Buy transactions have negative shares values (as low as−499.63), while every other transaction type in the dataset has only positive share values. What are two plausible business explanations for a negative share count on a Buy transaction (for example, a data-entry sign error versus a legitimate correction or reversal entry), and what would you do next to determine which explanation is more likely

Data-entry error
The transaction was meant to be for a normal purchase but they were entered as a negative number by mistake. 

Correction or reversal
They could be a reversal of a previously recorded purchase. If a purchase was done incorrectly, it could be the undoing of it. 

---
Cross Validation

Prompt A

Prompt B

6.What did each script return?
They both returned the same thing. they both returned 83,556. This matches the benchmark.

7. Do the results agree? If not, which one is wrong and why?
Yes, the results agree. 

8. Why is it useful to verify a count using subtraction rather than direct filtering?

They both use different logic so if they both result in the same number, it is unlikely there is an eror. 