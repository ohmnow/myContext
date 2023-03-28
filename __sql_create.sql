-- Create the 'personas' table
CREATE TABLE personas (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    branded_name VARCHAR(255) NOT NULL,
    attributes JSONB NOT NULL
);

-- Create the 'user_preferences' table
CREATE TABLE user_preferences (
    id UUID PRIMARY KEY,
    user_id UUID NOT NULL,
    category VARCHAR(255) NOT NULL,
    value VARCHAR(255) NOT NULL
);

-- Create the 'user_profiles' table
CREATE TABLE user_profiles (
    user_id UUID PRIMARY KEY,
    persona_id UUID,
    FOREIGN KEY (persona_id) REFERENCES personas(id)
);

-- Create the 'user_profile_preferences' table to establish a many-to-many relationship between user_profiles and user_preferences
CREATE TABLE user_profile_preferences (
    user_profile_id UUID NOT NULL,
    user_preference_id UUID NOT NULL,
    PRIMARY KEY (user_profile_id, user_preference_id),
    FOREIGN KEY (user_profile_id) REFERENCES user_profiles(user_id),
    FOREIGN KEY (user_preference_id) REFERENCES user_preferences(id)
);
