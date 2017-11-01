WebTelemetryBoto shell profile switch
==================================

Quickly switch AWS environment variables for boto management.
    AWS_ACCESS_KEY_ID
    AWS_SECRET_ACCESS_KEY
    AWS_ACCOUNT  --> Used for Shell Prompt description


Installation:
-------------
  run ./install.sh  # CWD must be in the same directory as source

  The installer will install .agboto_profile and .agboto_activate to ~/


Configuration:
--------------
  Edit .agboto_activate to add your AWS Access IDs and Secret Keys
  to the appropriate function

  example:

  function dev()  # WebTelemetryDev
  {
        AWS_ACCESS_KEY_ID=<your_WebTelemetryDev_Key>
        AWS_SECRET_ACCESS_KEY="<your_WebTelemetryDev_Secret>"
        AWS_ACCOUNT=WebTelemetryDev
  }

  Remove or modify additional functions as needed.
  Update .agboto_profile alias section if adding new accounts not yet listed.


Usage:
------
  To activate an account:
   % boto_activate.<account_alias>

  Example: activating Dev:
   % boto_activate.dev

  Tab shell completion will show available alias commands.
