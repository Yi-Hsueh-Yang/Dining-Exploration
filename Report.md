# Final Project Report

**Project URL**: https://github.com/CMU-IDS-Spring-2024/final-project-team3
**Video URL**: https://drive.google.com/file/d/1rH5iG6-8gN69FKj8zXdEFZ9L2fPKk8CN/view

The objective of this project is to develop an interactive application using Yelp's comprehensive dataset to address the challenges faced by both customers and business owners in navigating the business landscape of Nevada. The application provides actionable insights for users seeking businesses tailored to their preferences, empowering them to make informed decisions when choosing where to go. For business owners, the application offers valuable information on optimal locations for new ventures and essential business insights. The system utilizes various data science methods such as data preprocessing, filtering, mapping, and predictive modeling to achieve its goals. Through intuitive visualizations and interactive features, users can explore businesses effectively, receive personalized recommendations, and gain insights into business performance and potential check-in volumes. 


The application not only enhances the user experience by providing a comprehensive platform for exploration but also assists business owners in making strategic decisions to maximize their success. By leveraging Yelp's dataset and advanced data science techniques, this solution addresses the complex challenges of navigating the business landscape, ultimately empowering both customers and business owners with actionable insights and facilitating informed decision-making.

## Introduction

In today's dynamic business landscape, navigating the myriad of options poses a challenge for consumers and business owners. Customers often struggle to discern which areas host specific types of popular businesses and where to find establishments with the most favorable reviews. Simultaneously, business owners face the daunting task of identifying optimal locations to establish new ventures while understanding the competitive landscape and prevailing consumer preferences.


Leveraging the comprehensive Yelp database, we aim to tackle these challenges head-on by providing customers and business owners with actionable insights. Our mission is to empower consumers with knowledge about the business scene in Nevada, enabling informed decisions when picking places to go. Likewise, we strive to equip business owners with valuable information regarding lucrative locations for new business ventures and essential business insights about those areas.

## Related Work

Current research or work related to Yelp datasets covers a wide range of topics, most related to data visualization and machine learning [1][2].


Researchers have employed techniques like natural language processing (NLP) and machine learning to understand customer sentiment towards different businesses and services. Researchers have also developed recommendation systems based on Yelp data to help users discover new businesses and services. These systems often use collaborative filtering and content-based approaches to recommend businesses based on user preferences and past behavior. In addition, researchers have developed algorithms to detect and filter out fake reviews. Topic modeling techniques such as Latent Dirichlet Allocation (LDA) have been used to extract topics from Yelp reviews. 


As our project is an interactive app, designed to serve real customers and businesses, previous research on machine learning provides a lot of insights[3], especially for the business side of work. However, since the scope of our project is limited to NV state and the target audience is somewhat different from the traditional ML research, most of the design and visualizations in this project are based on the previous assignments and lectures of the course. 



## Methods

In this application, we utilized multiple data science methods in order to create an interactive Streamlit app for both the users and the business. We did some data preprocessing to get the 4 datasets that we needed and fit the requirements of our application including missing data imputation, outliers detection, filtering, mapping, and joining. For most parts of the functionalities in the app, we utilized filtering heavily, as our dataset is pretty huge, it is not representing or informative if plotting everything, thus, many toggles, bars-type of filters are created for the user or business to filter based on their needs to discover any hidden patterns and insights. 


On page 4, we included a predictive model for the number of check-ins that will be received by a business based on the category, location and weekly opening hours of a business. 


For data processing and transforming, we formed the feature vector by encoding each of these three inputs. The ‘category’ column is first separated and cleaned into a list and then converted to a one-hot encoding with sklearn’s MultiLabelBinarizer. The ‘city’ column is directly transformed into a one-hot encoding using panda’s get_dummies function. And the weekly opening hours are formed by extracting and summing over the daily hours from the ‘hours’ column. During processing, it is found that a significant portion (1358 out of 6570) of the businesses have unknown opening hours, and these numbers are set to the mean value of other businesses with valid opening hours.


For model training, we used the XGBoost library which provides efficient models for regression and classification tasks with high dimension data, and we set the train/test split to 0.8:0.2. The labels (y) were also transformed with logarithms to mitigate possible negative predictions when inferencing the model.

## Results

Page 1 serves as a comprehensive platform for customers to explore businesses tailored to their preferences. It boasts an array of filters, empowering users to refine their search based on criteria such as city, review rating, review count, optimal visit times, and relevant category keywords. To enhance user engagement, we employ intuitive visual representations: (1) Pictographs for Review Stars: Review stars are depicted through pictographs, offering users a quick and intuitive understanding of business ratings. (2) Bar Charts for Review Counts: Review counts are graphically represented using bar charts, facilitating a visual comparison of business popularity. Consider the scenario of a potential customer seeking a car wash facility in Sparks city on a specific Saturday afternoon at 13:15. Utilizing the available filters, they can seamlessly narrow down their options to businesses that meet their precise requirements. Should indecision persist, a convenient "random business" button is at their disposal, providing a serendipitous selection that aligns with all specified filter criteria.


Page 2 of the application serves as a recommender system designed to assist users who are having difficulty finding a restaurant to dine at. This system functions by comparing ratings between different restaurants to generate a curated list of recommended establishments of a specified type for the user, along with displaying their locations on an interactive map. Users have the option to toggle whether they want to view the latest reviews alongside the recommendations. The map feature is interactive, allowing users to explore and locate recommended restaurants conveniently. Each recommended restaurant on the map is labeled, enabling users to make informed decisions about which restaurant they would like to visit based on their preferences and location. This integrated approach provides users with a user-friendly experience in selecting a restaurant suited to their tastes and convenience.


Page 3 is designed for the platform business owner, e.g. Yelp, to quickly understand how their clients(the registered business in their app) are doing in terms of ratings and feedback scores. One possible scenario would be Yelp would like to know how restaurants are doing in the city of Reno during the year 2020, the map with businesses selected are pinned out along with their corresponding ratings during the time. Colors and icons are there to help distinguish the different performances of business. The platform can leverage the gathered here for their downstream services, e.g. to consider whether to provide promotions or advertisements to customers in certain areas, to adjust the distribution of their business, etc. The dashboard provides the business platform with multiple different categories and time ranges to choose from, there are even two distinct metrics that serve as different evaluation criteria, ratings(stars given by customers who went to certain stores at a certain time) and feedback_score(a normalized score calculating the average of normalized compliment votes and normalized review counts for each store).


Page 4 is designed for viewing and predicting check-in metrics of existing businesses, where a user can view the density of check-ins filtered by cities and time from the map. It is intended to show a potential business owner how the geographical location may affect the number of customers over time. For users that seek to open new businesses in the area, we also provide a predictive model to give advice on their choices. Based on the categories, location and opening hours users wish to have in their businesses, the model can provide an estimate of check-in’s to evaluate their plan, helping them make decisions and adjust strategies. For example, a new business owner may want to open an Italian restaurant, planning to operate 6 hours each day but considering which city to start with. The application will provide a prediction of check-ins based on the data provided by the owner, which helps the owner compare over different cities and make a final decision.

## Discussion

With page1, the audience has learned how to explore businesses effectively in using interactive filters. They've gained insights into the distribution of businesses across different cities and their popularity based on star ratings and review counts. Additionally, the option to select a random business has encouraged users to discover new places they might not have considered otherwise. This system has enabled the audience to make informed decisions about where to visit based on their preferences and the businesses' attributes. The audience might find themselves spending more time exploring different businesses and enjoying the element of surprise when discovering new places through the random business feature.


Page 2 of the application is designed to provide users with valuable insights to assist them in deciding which restaurant to visit. By combining recommended restaurant lists with detailed information and the latest reviews, users can assess the reliability of the recommendations and make informed choices. The interactive map feature enhances this experience by displaying the locations of recommended restaurants relative to the user's current position. This enables users to easily identify nearby options aligned with their preferences and the provided recommendations. The integration of restaurant details, reviews, and interactive mapping empowers users to select a restaurant that best suits their preferences and proximity, enhancing their overall dining experience.


For page 3, it was not intuitive to show the whole graph without filters, the audience is expected to see some interesting patterns as filters are applied. The audiences are encouraged to play along the filter bars and multi-selection boxes, to observe the performance of businesses within a location in a given time. The performance of which can sometimes tell the food preference changes across time in an area if the trend of ratings decreases for a kind of food. If not obvious, we can still observe the discrepancy in performance among all similar businesses. The user from the business side may find it useful to observe the different situations under different filters and design different marketing strategies accordingly.


Page 4 could help users gain multiple insights with the check-in data. First of all, users learn about the patterns of customer check-ins at various businesses across different cities and times, which helps them understand peak business hours and seasonal variations in customer behavior. Second, the application helps business owners explore the impact of geographical location on attracting customers. Users can see which areas are hotspots and which are not as frequented by viewing the density of check-ins on the map. Finally, the application serves as a decision support tool by providing predictions on potential check-in volumes for new businesses based on specified categories, locations, and operating hours. Overall speaking, the page enables business owners to make more informed decisions and plan wisely when setting up their business.

## Future Work

The current application could be further extended and refined in terms of both functionality and visualization. 


For page1, two points are identified for further work: (1) Instead of a conventional tabular layout, it is better to present the current business results in a more engaging manner. Each business could be represented as an individual block, showcasing its name. Upon hovering over each block, users could access related information about the business, fostering a more interactive experience.. (2) The current map lacks interactivity and fails to provide additional insights into the listed businesses. Future iterations could explore adding interactive features to the map. For example, users could click on map markers to view featured photos and reviews of the corresponding businesses, enriching their exploration experience.


Looking ahead to future improvements for page 2, there are three main areas to focus on. Firstly, enhancing the ranking system by incorporating additional factors beyond ratings, such as user preferences, cuisine variety, and service quality, can provide more accurate and relevant restaurant recommendations. Secondly, prominently displaying the user's location on the map in a distinct color will help users understand their current position within the application interface, enhancing usability. Lastly, leveraging user search history analysis to personalize recommendations based on individual preferences and behaviors can optimize the dining experience, ensuring that users receive tailored suggestions that align closely with their interests. These enhancements aim to refine the restaurant recommendation system, making it more intuitive, personalized, and effective for users.


For page 3, some additional improvements can be made to escalate the user experience and overall usefulness including (1) Add the fields for attributes for the filter, (2) Overall design, (3)Error handling for multiple filters. 


For functionality, adding the attributes field to the filter is expected to take the analysis one step further, the attributes field provides more information about the business, e.g. whether it accepts credit cards, whether there are bike parking places, whether they offer restaurant deliveries, etc. It would be better if the overall design of the dashboard could be consistent, considering sticking to a theme throughout all pages which can make the entire application more user-friendly. Although the filters are useful and are able to provide lots of unpredictable results, users may encounter errors such as applying too many filters to the data which ends up making the result empty and causing the page to fail. 


On page 4, there are some possible improvements regarding each subsection. For the check-in heatmap section, it would be better if the map could include icons for hotspots like tourist attractions and shopping malls, which would be beneficial for business owners to identify places that have a higher possibility of attracting customers. For the predictive model, the feature engineering part could be improved by mapping categories to a smaller subset that is more conclusive, reducing the number of features obtained from categories. Encoding of geographical information could be improved by seeking external data sources such as distance to downtown/hotspots, average income of people in the area, population of the city, etc.

## References

- 1. Yelp Analysis and Recommendation: https://github.com/electronic-pig/Yelp-Analysis-and-Reco_frontend?tab=readme-ov-file
- 2. Machine Learning and Visualization with Yelp Dataset: https://medium.com/@zhiwei_zhang/final-blog-642fb9c7e781
- 3. List of Research Papers on Yelp Dataset, mostly on ML topics: https://paperswithcode.com/dataset/yelp