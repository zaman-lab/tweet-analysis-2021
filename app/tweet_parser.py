


from app.bq_service import generate_timestamp

def parse_timeline_status(status):
    """
    Param status (tweepy.models.Status)

    Converts a nested status structure into a flat row of non-normalized status and user attributes.
    """

    if hasattr(status, "retweeted_status") and status.retweeted_status:
        retweeted_status_id = status.retweeted_status.id_str
        retweeted_user_id = status.retweeted_status.user.id
        retweeted_user_screen_name = status.retweeted_status.user.screen_name
    else:
        retweeted_status_id = None
        retweeted_user_id = None
        retweeted_user_screen_name = None

    user = status.user
    row = {
        "user_id": user.id_str,
        "status_id": status.id_str,
        "status_text": parse_string(parse_full_text(status)),
        "created_at": generate_timestamp(status.created_at),

        "geo": status.geo,
        "is_quote": status.is_quote_status,
        "truncated": status.truncated,

        "reply_status_id": status.in_reply_to_status_id_str,
        "reply_user_id": status.in_reply_to_user_id_str,
        "retweeted_status_id": retweeted_status_id,
        "retweeted_user_id": retweeted_user_id,
        "retweeted_user_screen_name": retweeted_user_screen_name,

        "lookup_at": generate_timestamp()
    } # the order of these columns matters, when inserting records to BQ, based on the schema definition
    return row

def parse_string(my_str):
    """
    Removes line-breaks for cleaner CSV storage. Handles string or null value. Returns string or null value

    Param my_str (str)
    """
    try:
        my_str = my_str.replace("\n", " ")
        my_str = my_str.replace("\r", " ")
        my_str = my_str.strip()
    except AttributeError as err:
        pass
    return my_str

def parse_full_text(status):
    """Param status (tweepy.models.Status)"""
    # GET FULL TEXT
    # h/t: https://github.com/tweepy/tweepy/issues/974#issuecomment-383846209

    if hasattr(status, "full_text"):
        full_text = status.full_text
    elif hasattr(status, "extended_tweet"):
        full_text = status.extended_tweet["full_text"]
    else:
        full_text = status.text

    return full_text
