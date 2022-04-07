# MSiA423 Hotel Booking Cancellation Prediction

Developer: Jia Hao Lo

## Project Charter

### Vision
The project aims to predict the cancellation of hotel booking for the hotels  to carry out demand prediction, customer retention and profit maximization. The key drivers for booking cancelation will also be identified for the hotel to understand the patterns and reasons for cancellation, and act accordingly based on the insights.

### Mission
The project will build a predictive model to predict whether a hotel booking will be cancelled based on details of the booking provided by the user, and identify key drivers of hotel booking cancellation. The data is extracted from Hotel Booking Demand Datasets written by Nuno Antonio, Ana de Almeida and Luis Nunes.

Source:

Nuno Antonio, Ana de Almeida, Luis Nunes,
Hotel booking demand datasets,
Data in Brief,
Volume 22,
2019,
Pages 41-49,
ISSN 2352-3409,
https://doi.org/10.1016/j.dib.2018.11.126.
(https://www.sciencedirect.com/science/article/pii/S2352340918315191)
https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand?resource=download

Abstract: This data article describes two datasets with hotel demand data. One of the hotels (H1) is a resort hotel and the other is a city hotel (H2). Both datasets share the same structure, with 31 variables describing the 40,060 observations of H1 and 79,330 observations of H2. Each observation represents a hotel booking. Both datasets comprehend bookings due to arrive between the 1st of July of 2015 and the 31st of August 2017, including bookings that effectively arrived and bookings that were canceled. Since this is hotel real data, all data elements pertaining hotel or costumer identification were deleted. Due to the scarcity of real business data for scientific and educational purposes, these datasets can have an important role for research and education in revenue management, machine learning, or data mining, as well as in other fields.


### Success Criteria

1. Machine Learning Performance Metric:

   F1-score will be used as the model evaluation metric. The final model with cross-validation F1-score more than 0.9 will be  selected for deployment.

2. Business Outcome Metric:

    * Cost reduction from optimizing wasted resources on cancelled booking

    * Revenue increment from preventing cancellation by addressing the key drivers accordingly.


