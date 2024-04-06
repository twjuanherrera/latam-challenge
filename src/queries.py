"""
The top 10 dates with the most tweets. Mention the user (username) with the most posts for each of those days.
"""
top_10_users_and_dates = r"""
    WITH 
    TopDates AS (
        SELECT
            CAST(date AS DATE) AS tweets_date,
            COUNT(*) AS tweet_count
        FROM tweets_dataset.tweets
        GROUP BY tweets_date
        ORDER BY tweet_count DESC
        LIMIT 10
    ),
    TopUsersDate AS (
        SELECT
            TD.tweets_date,
            TW.user.username,
            MAX(TD.tweet_count) AS max_tweet_count,
            COUNT(*) AS user_tweet_count,
            ROW_NUMBER() OVER (
                PARTITION BY TD.tweets_date 
                ORDER BY MAX(TD.tweet_count) DESC, COUNT(*) DESC
            ) AS row_number
        FROM tweets_dataset.tweets AS TW
        INNER JOIN TopDates AS TD
            ON TD.tweets_date = CAST(TW.date AS DATE)
        GROUP BY
            TD.tweets_date,
            TW.user.username
        ORDER BY
            max_tweet_count DESC,
            user_tweet_count DESC,
            TW.user.username ASC
    )

    SELECT
        tweets_date,
        username
    FROM TopUsersDate
    WHERE row_number = 1
"""