# What Makes a House a Home in King County Washington?
**A Linear Regression Model to Predict the Price of a Home**    


## Table of Contents
* I. Introduction
* II. Navigating the Repository
* III. Methodology
* IV. Conclusions

## I. Introduction
For this project, I will perform an analysis of the King County housing data set. My objective is to design a linear regression model that will predict the price the of a home in King County, given certain features.

King County is located in the state of Washington in the United States. Washington is a coastal in the Pacific North West, and is part of the greater Seattle area. It is a diverse county, with rural, suburban, and urban areas. The data set included data from 70 different zipcodes.     

![King County Zip Code Map](kc_zip_map.png "King County Zip Code Map")   

In this data set, I was provided with the following features:   
* id (a unique identification number for each home)
* date (the date of sale)
* price (the selling price)
* bedrooms (the number of bedrooms)
* bathrooms (the number of bathrooms)
* sqft_living (square footage of the living square)
* sqft_lot (square footage of the lot)
* floors (the number of floors)
* waterfront (indicates if the property was a waterfront property, when available)
* view (indicates the amount of times the home was viewed)
* condition (a scale of 1-5 the indicates how well a home was maintained)
* grade (a scale of 1-13 that indicates the quality of the home, based on...)
* sqft_above (square footage above ground)
* sqft_basement (square footage below ground)
* yr_built (year the home was built)
* yr_renovated (year the home was rennovated)
* zipcode (home location zip code)
* lat (home location latitude)
* long (home location longitude)
* sqft_living15 (square footage of interior housing living space for the nearest 15 neighbors)
* sqft_lot15 (square footage of interior housing lot space for the nearest 15 neighbors)   

If you are interested in how King County determines the grade and condition of the property, take a look at page 33 this guide: <https://www.kingcounty.gov/depts/assessor/Reports/area-reports/2017/residential-westcentral/~/media/depts/assessor/documents/AreaReports/2017/Residential/013.ashx>      


## II. Navigating the Repo

| Filename        | Description   |
| :-------------  |:--------------|
| README.md       | a .md file that is a guide to this repository, the current document           |
| model.ipynb     | a jupyter notebook containg an earlier model, and technical details used to create it|
| improved_model.ipynb     | a jupyter notebook containg the model explained here, and technical details used to create it|
| functions1.py  | a .py file with collection of custom functions used in model.ipynb            |
| presentation.pdf| a .pdf file of the non-technical overview of this project                     |
| kc_zip_map.png  | a .png file with an image of King County zip code boundary map                |
| ols.png  | a .png of  results                |
| corr_matrix.png  | a .png of correlation matrix heatmap               |
| qqplot.png  | a .png file with qq plot of residuals               |
| distplot.png  | a .png file with a distplot of residuals                |
| regplot.png  | a .png file with a regplot of redisuals               |

## III. Methodology
For this anaylsis, the OSEMN methodology was used. For the purposes of this document, scrubbing data and exploring data were combined into one section.

### Hypothesis
The price of a home in King County can be predicted by distance from Seattle or Bellevue.


### 1. Obtaining Data
The original dataset can be found at: <https://raw.githubusercontent.com/learn-co-students/dsc-mod-2-project-v2-1-onl01-dtsc-pt-052620/master/kc_house_data.csv>.     

### 2. Scrubbing & Exploring Data
Outliers with a z-score over 3 were removed from  'price', 'bedrooms', 'bathrooms','sqft_living', 'grade'.    
From the original data a Box-Cox transformation was performed on 'price', 'sqft_living', 'sqft_lot', 'sqft_above', and 'sqft_basement'.    

Some features were eliminated.
| Feature     | Reason for Elimination |
|:---------   | :-----------|    
| data | There are only two years represented in this data set. |
| floors | To limit complexity, size will captured by other features. |
| sqft_lot | This analysis is going to focus on living space as a secondary factor.|
| sqft_lot15 | Location and size will be addressed by other features. |
| sqft_living15 | Location and size will be addressed by other features. |
| sqft_above | This information is captured by square foot living.|
| sqft_basement | Homes with no basement are represented by zero, creating a severe left skew. Considering that sqft_living is the sum of sqft_basement, and sqft_above, assigning sqft_basement with a binary variable will retain the information while eliminatig a problematic column. |
| yr_built | Unneccessary to test our hypothesis. |

#### Collinearity Check
The final features were tested for multicollinearity using a correlation matrix and heatmap.
![Correlation Matrix Heat Map](corr_matrix.png "Correlation Matrix Heat Map")

## 3. Modeling Data & Interpreting Data
Finally, the resulting data frame was trained and tested with an 70/30 split using OLS statsmodels.
![ols](ols.png "Correlation Matrix Heat Map") 


#### R-Squared/Adjusted R-Squared
At .823/.822, the model can be considered reasonably accurate, and the predictors can be considered relevant.

#### Coefficients
It appears from the coefficients that distance to Seattle or Bellevue is a very important predictor of price. The further away a home is from Seattle or Bellevue, the lower the price seems to go.

Another good indicator seems to be squarefoot of living space.

All of the zipcodes appear to be in a similar range, 

#### T-Values/P-Values
The t-values all seem high enough, with the sqft_living t-value being particularly high in the positive direction. The t-values for the zip codes all seem to be in different, but all the values seem to fall between 6 and 10. Condition is confirmed as being a fairly strong positive influence, while basements and too many bedrooms seem to be a negative influence. The p-values are all very close to zero, so we can trust the p-values. We can reject the null-hypothesis that proximity to Seattle/Bellevue is the most important predictor. 

#### Satisfying the Assumptions of Linear Regression
The data appears to be normally distributed.    
![qqplot](qqplot.png "QQ Plot") 
![displot](displot.png "Distplot")     

Homoscedacity seems to be fairly neutral based on the scatterplot.      
![regplot](regplot.png "Regplot")

## 4. Conclusions and Future Work

### Conclusions

#### 1. Start with location
Distance to Seattle/Bellevue is an important factor, and homes become more expensive as we move closer to either of these areas. Naturally, certain zipcodes seem to command the highest prices.

**Most Pricey Zipcodes, in Descending Order**

| Rank        | Zipcode     | City        | Notable Qualities                    |
|:---------   | :-----------| :-----------| :-----------                         | 
| 1           | 98039       | Medina      |  Waterfront zipcode outside Bellevue |
| 2           | 98040       | Mercer Island | Island between Seattle & Bellevue  |
| 3           | 98112       | Seattle/Madison Park | Waterfront neighnorhood in North East Seattle |
| 4           | 98102       | Seattle/East Lake/Capitol Hill | Waterfront neighborhood just West of Madison Park |
| 5           | 98119       | Seattle West Queen Anne/North Queen Anne | Waterfront neighnorhood in North West Seattle |
| 6           | 98109       | Seattle East Queen Anne/West Lake | Waterfront neighnorhood in North West Seattle, near Capitol Hill |
| 7           | 98122       | Seattle Central District | North east Seattle, below Madison Park |
| 8           | 98005       | Crossroads | Just east of Bellevue
| 9           | 98199       | Magnolia | North-West Peninsula of Seattle
| 10          | 98006       | Factoria | Just South of Bellevue |

#### 2. Focus on size
Square footage of living space was also an important factor, and in certain zipcodes, a small increase square footage is leading to large increase in price.

#### 3. Pay Attention to Function
More bedrooms in a home can indicate less functional, smaller bedrooms if there is not a sufficient increase in square feet of living space. In addition, the presence of a basement indicates that total above ground living space could be as much as 50% of the entire living space. Having that square footage below ground can be less functional for home owners. Having more space above ground for functions that could be carried out in a basement like a laundry room, storage, or den, is more desirable above ground. I can also imagine that in a coastal city, a basement can be a huge liability. Above ground square footage is worth more, and the functionality of the home's layout is an important contributor.

# Future Work
I think that this analysis could be improved if population data were included in for each zipcode. It is unclear what effect population might have on price. For example, a zipcode that skews more affluent might have a lower population, however the affluent quality of the neighborhood has a more significant increase on price. There is also an argument to be made that in more crowded areas, the price per square foot might be higher as well.  It is possible that using median incomes in addition to population might reveal more about the role population.

In addition in order to expand on the role of location, I think that the lattitude and longitude data would be a useful feature to explore the proximity between a home and Seattle. One hypothesis is that there is an association between income, population, and proximity to Seattle that would influence what a buyer would be willing to pay for a house.

It might also be interesting to see how fluctuations in population and incomes might predict how housing prices might rise or fall over time.
