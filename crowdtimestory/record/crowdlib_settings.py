#!/usr/local/bin/python2.9

from crowdlib import settings as cls #, os

# SERVICE TYPE
cls.service_type = "sandbox"  # REQUIRED; must be either "sandbox" or "production"

# AWS ACCOUNT INFO
cls.aws_account_id  = ""                     # REQUIRED; "Access Key ID" from AWS
cls.aws_account_key = "" # REQUIRED; "Secret Access Key" from AWS

# DIRECTORY FOR CROWDLIB DATABASE
#cls.db_dir = os.path.abspath(os.path.expanduser("~/.crowdlib_data/"))  # Optional; this is the default

# DEFAULT PARAMETERS used when creating HITs
cls.default_autopay_delay              = 60*60*8   # Optional; auto-pay after 8 hours; default is 7 days
cls.default_reward                     = 0.01       # Optional; no default (i.e., specify each time)
cls.default_lifetime                   = 60*60*24*1 # Optional; available up to 1 day (same as default)
cls.default_max_assignments            = 1          # Optional; 1 judgment (same as default)
cls.default_time_limit                 = 60*5      # Optional; auto-return after 5 mins (same as default)
cls.default_qualification_requirements = ()         # Optional; default is no qualification requirement
cls.default_requester_annotation       = ""         # Optional; default is no requester annotation
cls.default_keywords                   = ()         # Optional; default is no keywords