# Formats a string by taking every "{FormatName}" and looking up this field in "name1.name2" if key is "name1.name2.name3" and inserting this instead
# Value (str): The string to format
# Key (str): The key for this string
# Settings (lab.setting): The setting which this is found in
def formatString(Value, Key, Settings):
    # Get the sub settings
    SubSettings = Settings.getBranch(str(Key).rsplit(".", 1)[0])
    
    # Format the sequence
    Name = str(Value).split("_", 1)[0]
    SplitValue = str(Value).split("{")
    NewValue = SplitValue[0]

    for FormatString in SplitValue[1:]:
        # Find end
        FormatName, Leftover = FormatString.split("}", 1)
        
        # Get the format
        FormatValue = SubSettings[f"{Name}.{FormatName}"]
    
        NewValue = f"{NewValue}{FormatValue}{Leftover}"
        
    return NewValue