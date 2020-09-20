{
 "cells": [
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# What Makes a House a Home in King County Washington?\n",
    "**A Linear Regression Model to Predict the Price of a Home**    \n",
    "*by Christine Egan*\n",
    "\n",
    "## Table of Contents\n",
    "* I. Introduction\n",
    "* II. Navigating the Repository\n",
    "* III. Methodology\n",
    "* IV. Conclusions"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## I. Introduction\n",
    "For this project, I will perform an analysis of the King County housing data set. My objective is to design a linear regression model that will predict the price the of a home in King County, given certain features.\n",
    "\n",
    "King County is located in the state of Washington in the United States. Washington is a coastal in the Pacific North West, and is part of the greater Seattle area. It is a diverse county, with rural, suburban, and urban areas. The data set included data from 70 different zipcodes.     \n",
    "\n",
    "![King County Zip Code Map](kc_zip_map.png \"King County Zip Code Map\")   \n",
    "\n",
    "In this data set, I was provided with the following features:   \n",
    "* id (a unique identification number for each home)\n",
    "* date (the date of sale)\n",
    "* price (the selling price)\n",
    "* bedrooms (the number of bedrooms)\n",
    "* bathrooms (the number of bathrooms)\n",
    "* sqft_living (square footage of the living square)\n",
    "* sqft_lot (square footage of the lot)\n",
    "* floors (the number of floors)\n",
    "* waterfront (indicates if the property was a waterfront property, when available)\n",
    "* view (indicates the amount of times the home was viewed)\n",
    "* condition (a scale of 1-5 the indicates how well a home was maintained)\n",
    "* grade (a scale of 1-13 that indicates the quality of the home, based on...)\n",
    "* sqft_above (square footage above ground)\n",
    "* sqft_basement (square footage below ground)\n",
    "* yr_built (year the home was built)\n",
    "* yr_renovated (year the home was rennovated)\n",
    "* zipcode (home location zip code)\n",
    "* lat (home location latitude)\n",
    "* long (home location longitude)\n",
    "* sqft_living15 (square footage of interior housing living space for the nearest 15 neighbors)\n",
    "* sqft_lot15 (square footage of interior housing lot space for the nearest 15 neighbors)   \n",
    "\n",
    "If you are interested in how King County determines the grade and condition of the property, take a look at page 33 this guide: <https://www.kingcounty.gov/depts/assessor/Reports/area-reports/2017/residential-westcentral/~/media/depts/assessor/documents/AreaReports/2017/Residential/013.ashx>      \n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<style>\n",
       "table {float:left}\n",
       "</style>\n"
      ],
      "text/plain": [
       "<IPython.core.display.HTML object>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "%%html\n",
    "<style>\n",
    "table {float:left}\n",
    "</style>"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## II. Navigating the Repo\n",
    "\n",
    "| Filename        | Description   |\n",
    "| :-------------  |:--------------|\n",
    "| README.md       | a .md file that is a guide to this repository, the current document           |\n",
    "| model.ipynb     | a jupyter notebook containg the model, and technical details used to create it|\n",
    "| my_function.py  | a .py file with collection of custom functions used in model.ipynb            |\n",
    "| my_functions.md | a .md file with a description of the custom functions in my_functions.py      |\n",
    "| presentation.pdf| a .pdf file of the non-technical overview of this project                     |\n",
    "| kc_zip_map.png  | a .png file with an image of King County zip code boundary map                |\n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## III. Methodology\n",
    "For this anaylsis, the OSEMN methodology was used. For the purposes of this document, scrubbing data and exploring data were combined into one section.\n",
    "\n",
    "### 1. Obtaining Data\n",
    "The original dataset can be found at: <https://raw.githubusercontent.com/learn-co-students/dsc-mod-2-project-v2-1-onl01-dtsc-pt-052620/master/kc_house_data.csv>.     \n",
    "\n",
    "### 2. Scrubbing & Exploring Data\n",
    "From the original data, certain features were retained, modified, added, and removed."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Retained / Transformed\n",
    "| Feature    | Description of Action |\n",
    "|:---------  | :-----------|\n",
    "|id          | Some id numbers appeared twice, with different date values, indicating the same home being sold more than once in the same two year period. Duplicate id entries were removed, keeping the first sale.|\n",
    "|date        | Transformed to datetime object from a string. |\n",
    "|price       | Outliers with a z-score greater than 3 were removed.|\n",
    "|sqft_living | Full retained. |      \n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Modified\n",
    "| Feature     | Description of Action |\n",
    "|:---------   | :-----------|\n",
    "|bedrooms     | Outliers with z-score greater than 3 were removed. Then, it was used to create the feature '4_plus_bedrooms', which contained 0 or 1 to indicate if there were more or less than 4 bedrooms. |\n",
    "|bathrooms    | Outliers with z-score greater than 3 were removed. Then, it was used to create the feature '3_plus_bathrooms', which contained 0 or 1 to indicate if there were more or less than 3 bathrooms. |\n",
    "|grade        | It was used to create the feature '8_plus_grade', which contained a 0 or 1 to indicate if the grade was more or less than 8. \n",
    "|sqft_basement| Because properties without a basement were represented by zero square feet, it created an exetreme left skew. To remedy, it was transformed into the feature 'basement' with a 0 or 1 to indicate the absence or presence of a basement.|\n",
    "|yr_built     | Transformed to create 'age_at_sale' using 'date'.\n",
    "|zipcode      | Transformed to create the features 'zip_avg_price', 'zip_avg_sqft', 'zip_avg_pp_sqft' using 'price.' |\n",
    "|sqft_living  | Combined with 'price' to create 'price_per_sqft'. |     "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Created\n",
    "| Feature     | Description of Feature |     \n",
    "|:---------   | :-----------|\n",
    "| 4_plus_bedrooms  | Indicates with a 0 or 1 if there are more than 4 bedrooms. |\n",
    "| 3_plus_bathrooms | Indicates with a 0 or 1 if there are more than 3 bathrooms. |\n",
    "| 8_plus_grade     | Indicates with a 0 or 1 if the grade is greater than 8. |\n",
    "| basement         | Indicates with a 0 or 1 if the presence of a basement. |\n",
    "| age_at_sale      | Indicates the age of a property on the date of sale. |\n",
    "| zip_avg_price    | Indicates the average price for a property by zipcode. |\n",
    "| zip_avg_sqft     | Indicates the average of 'sqft_living' per zipcode. |\n",
    "| zip_avg_pp_sqft  | Indicates the average price per square foot per zipcode. |        "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Eliminated\n",
    "| Feature     | Reason for Elimination |\n",
    "|:---------   | :-----------|\n",
    "| yr_renovated | There was a lot of missing data, making it an unsuitable predictor. |\n",
    "| floors       | This information was redundant, and similar information could be obtained by examining square footage and number of rooms. |\n",
    "| waterfront   | There was a lot of missing data, making it an unsuitable predictor. |\n",
    "| view         | There was a lot of missing data, making it an unsuitable predictor. |\n",
    "| lat          | Not needed for this analysis. |\n",
    "| long         | Not needed for this analysis |\n",
    "| sqft_above   | This information was redundant, and similar information could be obtained by examining square footage and number of rooms. |\n",
    "| sqft_basement| The skew of this information was severe, so it was used to create a more useful feature, then dropped. |\n",
    "| sqft_lot     | Exetreme outliers made this data fairly unreliable, and efforts to normalize compromised the accuracy of the results. |\n",
    "| sqft_living15| Demonstrated high correlation with more useful square foot metrics, such as 'sqft_living'.\n",
    "| sqft_lot15   | The elimination of other features made it irrelevant for analysis.     "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Final Features\n",
    "The objective of this model was to test which features have a significant influence on the price of a home in King County. To facilitate this, features were chosen to reflect, the size of the home, the age of the home, the quality of the home, and the location of the home.  \n",
    "\n",
    "| Feature                | Indicates:                                 |\n",
    "|:---------              | :-----------                               |\n",
    "| sqft_living            |  size                                      |\n",
    "| price_per_sqft_living  |  a relationship between size and price     |\n",
    "| zip_avg_price          |  a relationship between location and price |\n",
    "| zip_avg_sqft           |  a relationship between size and location  |\n",
    "| age_at_sale            |  age                                       |\n",
    "| zip_age_avg_price      |  a relationship between age and price      |\n",
    "| 4_plus_bedrooms        |  size                                      |\n",
    "| 3_plus_bathrooms       |  size                                      |\n",
    "| 8_plus_grade           |  quality                                   |\n",
    "| basement               |  size                                      |   "
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### Collinearity Check\n",
    "The final features were tested for multicollinearity using a correlation matrix and heatmap.\n",
    "![Correlation Matrix Heat Map](corr_map.png \"Correlation Matrix Heat Map\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "## 3. Modeling Data\n",
    "Finally, the resulting data frame was trained and tested with an 70/30 split using OLS statsmodels. This generated the following summary."
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "![OLS Results](ols_results.png \"OLS Summary\")"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "### 4. Interpreting the Data"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "#### R-squared / Adjusted R-squared\n",
    "The R-squared value and adjusted R-squared value speak to the accuracy of the model and the relevance of the data. Simplyfing categorical features using binary categories allowed the data from those categories to be used, without creating unncessary complexity. As a result, the R-squared value and the Adjusted R-squared value are identical, indicating that each of the predictors are relevant.\n",
    "\n",
    "#### Coefficients\n",
    "| Feature                | Indicates:                                 |\n",
    "|:---------              | :-----------                               |\n",
    "| sqft_living            |  As square footage increases, the mean price increases. |                               \n",
    "| price_per_sqft_living  |  As price per square foot increases, the mean price increases.|\n",
    "| zip_avg_price          |  As price per square foot increases, the mean price increases. |\n",
    "| zip_avg_sqft           |  As the zipcode average sqft decreases, the mean price tends to increase.  |\n",
    "| age_at_sale            |  As age at sale increases, the mean price increases. |\n",
    "| zip_age_avg_price      |  As a zipcode's average price by age decreases, the mean price increases. |\n",
    "| 4_plus_bedrooms        |  When there are more than 4 bedrooms, the mean price descreases.|\n",
    "| 3_plus_bathrooms       |  When there are more than 3 bathrooms, the mean price increases. |\n",
    "| 8_plus_grade           |  An increase in grade is associated with an increase in the mean price. |\n",
    "| basement               |  When there is a basement, mean price increases.|   \n"
   ]
  },
  {
   "cell_type": "markdown",
   "metadata": {},
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:learn-env] *",
   "language": "python",
   "name": "conda-env-learn-env-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.6.10"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
