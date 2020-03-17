# Online News Popularity

This dataset summarizes a heterogeneous set of features about articles published by Mashable in a period of two years.
The goal is to predict the number of shares in social networks (popularity).
[[Source]](https://archive.ics.uci.edu/ml/datasets/Online+News+Popularity)

## Samples

Number of samples: 39,644.

## Variables

| Numerical | Categorical | Binary | Total |
| :--- | :--- | :--- | :--- |
| 46 | 1 | 14 | 61 |

| Predictive | Non-Predictive | Target | Total |
| :--- | :--- | :--- | :--- |
| 58 | 2 | 1 | 61 |

The variable index corresponds to the order in the original data.

The corresponding feature index after the transformation may differ (check the metadata).

The "url" and "timedelta" variables are ignored.

The binary variables with the "data_channel" prefix belong to the same one-hot-encoding.

The binary variables with the "weekday" prefix belong to the same one-hot-encoding.

The target variable is "shares".

| Index | Name | Type | Description |
| :--- | :--- | :--- | :--- |
| 1 | url | categorical | URL of the article. |
| 2 | timedelta | numerical | Days between the article publication and the dataset acquisition. |
| 3 | n_tokens_title | numerical | Number of words in the title. |
| 4 | n_tokens_content | numerical | Number of words in the content. |
| 5 | n_unique_tokens | numerical | Rate of unique words in the content. |
| 6 | n_non_stop_words | numerical | Rate of non-stop words in the content. |
| 7 | n_non_stop_unique_tokens | numerical | Rate of unique non-stop words in the content. |
| 8 | num_hrefs | numerical | Number of links. |
| 9 | num_self_hrefs | numerical | Number of links to other articles published by Mashable. |
| 10 | num_imgs | numerical | Number of images. |
| 11 | num_videos | numerical | Number of videos. |
| 12 | average_token_length | numerical | Average length of the words in the content. |
| 13 | num_keywords | numerical | Number of keywords in the metadata. |
| 14 | data_channel_is_lifestyle | binary | Is data channel 'Lifestyle'?. |
| 15 | data_channel_is_entertainment | binary | Is data channel 'Entertainment'?. |
| 16 | data_channel_is_bus | binary | Is data channel 'Business'?. |
| 17 | data_channel_is_socmed | binary | Is data channel 'Social Media'?. |
| 18 | data_channel_is_tech | binary | Is data channel 'Tech'?. |
| 19 | data_channel_is_world | binary | Is data channel 'World'?. |
| 20 | kw_min_min | numerical | Worst keyword (min. shares). |
| 21 | kw_max_min | numerical | Worst keyword (max. shares). |
| 22 | kw_avg_min | numerical | Worst keyword (avg. shares). |
| 23 | kw_min_max | numerical | Best keyword (min. shares). |
| 24 | kw_max_max | numerical | Best keyword (max. shares). |
| 25 | kw_avg_max | numerical | Best keyword (avg. shares). |
| 26 | kw_min_avg | numerical | Avg. keyword (min. shares). |
| 27 | kw_max_avg | numerical | Avg. keyword (max. shares). |
| 28 | kw_avg_avg | numerical | Avg. keyword (avg. shares). |
| 29 | self_reference_min_shares | numerical | Min. shares of referenced articles in Mashable. |
| 30 | self_reference_max_shares | numerical | Max. shares of referenced articles in Mashable. |
| 31 | self_reference_avg_sharess | numerical | Avg. shares of referenced articles in Mashable. |
| 32 | weekday_is_monday | binary | Was the article published on a Monday?. |
| 33 | weekday_is_tuesday | binary | Was the article published on a Tuesday?. |
| 34 | weekday_is_wednesday | binary | Was the article published on a Wednesday?. |
| 35 | weekday_is_thursday | binary | Was the article published on a Thursday?. |
| 36 | weekday_is_friday | binary | Was the article published on a Friday?. |
| 37 | weekday_is_saturday | binary | Was the article published on a Saturday?. |
| 38 | weekday_is_sunday | binary | Was the article published on a Sunday?. |
| 39 | is_weekend | binary | Was the article published on the weekend?. |
| 40 | LDA_40 | numerical | Closeness to LDA topic 40. |
| 41 | LDA_41 | numerical | Closeness to LDA topic 41. |
| 42 | LDA_42 | numerical | Closeness to LDA topic 42. |
| 43 | LDA_43 | numerical | Closeness to LDA topic 43. |
| 44 | LDA_44 | numerical | Closeness to LDA topic 44. |
| 45 | global_subjectivity | numerical | Text subjectivity. |
| 46 | global_sentiment_polarity | numerical | Text sentiment polarity. |
| 47 | global_rate_positive_words | numerical | Rate of positive words in the content. |
| 48 | global_rate_negative_words | numerical | Rate of negative words in the content. |
| 49 | rate_positive_words | numerical | Rate of positive words among non-neutral tokens. |
| 50 | rate_negative_words | numerical | Rate of negative words among non-neutral tokens. |
| 51 | avg_positive_polarity | numerical | Avg. polarity of positive words. |
| 52 | min_positive_polarity | numerical | Min. polarity of positive words. |
| 53 | max_positive_polarity | numerical | Max. polarity of positive words. |
| 54 | avg_negative_polarity | numerical | Avg. polarity of negative words. |
| 55 | min_negative_polarity | numerical | Min. polarity of negative words. |
| 56 | max_negative_polarity | numerical | Max. polarity of negative words. |
| 57 | title_subjectivity | numerical | Title subjectivity. |
| 58 | title_sentiment_polarity | numerical | Title polarity. |
| 59 | abs_title_subjectivity | numerical | Absolute subjectivity level. |
| 60 | abs_title_sentiment_polarity | numerical | Absolute polarity level. |
| 61 | shares | numerical | Number of shares. |

### Is weekend

Unique values: 2.

| Value | Samples |
| :--- | :--- |
| 0 | 34454 |
| 1 | 5190 |

### Data channel

Unique values: 7.

| Value | Samples |
| :--- | :--- |
| bus | 6258 |
| entertainment | 7057 |
| lifestyle | 2099 |
| none | 6134 |
| socmed | 2323 |
| tech | 7346 |
| world | 8427 |

### Weekday

Unique values: 7.

| Value | Samples |
| :--- | :--- |
| friday | 5701 |
| monday | 6661 |
| saturday | 2453 |
| sunday | 2737 |
| thursday | 7267 |
| tuesday | 7390 |
| wednesday | 7435 |
