# Bryan Swords

USE myTrip;

#######################################################################

# Sets name of entire trip, as well as when it will take place
CREATE TABLE Trip (title CHAR(30) NOT NULL,
                   start_date DATE NOT NULL,
                   end_date DATE NOT NULL,
                   PRIMARY KEY (title));

# Mimics Check Constraints on Trip since MySQL does not support them
DELIMITER $$
CREATE TRIGGER trip_trigger BEFORE INSERT ON Trip
  FOR EACH ROW 
  BEGIN
  
  # Cannot plan a trip before the current date/ end date cannot be before start date
  IF (NEW.start_date < CURDATE()) OR (NEW.end_date < NEW.start_date) 
  THEN
    SET NEW.start_date = NULL;

  END IF;
  END$$
DELIMITER ;

# Mimics Check Constraints on Trip since MySQL does not support them
DELIMITER $$
CREATE TRIGGER before_update_trip_trigger BEFORE UPDATE ON Trip
  FOR EACH ROW 
  BEGIN
  
  # Cannot plan a trip before the current date/ end date cannot be before start date
  IF (NEW.start_date < CURDATE()) OR (NEW.end_date < NEW.start_date) 
  THEN
    SET NEW.start_date = NULL;

  END IF;
  END$$
DELIMITER ;

####################################################################################

# Stores info on different locations that will be visited on trip
CREATE TABLE Location (lid CHAR(20) NOT NULL,   
                       lname CHAR(50) NOT NULL, # Ex: Tony's Pizzeria
					   street VARCHAR(60),      # Ex: 85 Main Street
                       lzip CHAR(20), 
                       PRIMARY KEY (lid),
                       FOREIGN KEY (lzip) REFERENCES Address (zip)
                                                 ON UPDATE CASCADE);


# Different table for this info to avoid redundant data storage
CREATE TABLE Address (zip CHAR(20) NOT NULL,
                      city VARCHAR(40) NOT NULL,
                      country CHAR(40) NOT NULL,
                      state CHAR(20) DEFAULT ' ',
					  PRIMARY KEY (zip, city));

#################################################################################

# Weak entity set to Travel
CREATE TABLE Activity (aname CHAR(20) NOT NULL,    # Ex: Dinner
                       descr VARCHAR(80) NOT NULL, # Ex: Eat dinner at Tonys and explore area
                       adate DATE NOT NULL,        
                       atime TIME NOT NULL,
                       trip CHAR(20) NOT NULL,
                       location CHAR(20) NOT NULL,
					   travel CHAR(20) NOT NULL,
                       PRIMARY KEY(descr, travel),
                       FOREIGN KEY (trip) REFERENCES Trip (title)
									         ON DELETE CASCADE
											 ON UPDATE CASCADE,
                       FOREIGN KEY (location) REFERENCES Location (lid)
                                                      ON UPDATE CASCADE,
                       FOREIGN KEY (travel) REFERENCES Travel (trid)
									        	ON DELETE CASCADE
                                                ON UPDATE CASCADE);




# Mimics Check Constraints on Activity since MySQL does not support them
DELIMITER $$
CREATE TRIGGER before_insert_activity_trigger BEFORE INSERT ON Activity
  FOR EACH ROW 
  BEGIN

  # Cannot plan an activity in the area user will not be at
  IF (SELECT lzip FROM Location WHERE Location.lid = NEW.location) != 
	 (SELECT lzip FROM Location WHERE Location.lid = 
	   (SELECT destination FROM Travel WHERE Travel.trid = NEW.travel))
  THEN
    SET NEW.location = NULL;

  # Cannot plan an activity outside the bounds of the trip
  ELSEIF ((NEW.adate < (SELECT start_date FROM Trip WHERE (Trip.title = NEW.trip))) OR
		   (NEW.adate > (SELECT end_date FROM Trip WHERE (Trip.title = NEW.trip))))
  THEN
    SET NEW.location = NULL;

  # Cannot plan an activity before the travel event that brings user to location
  ELSEIF (NEW.atime < (SELECT eta FROM Travel WHERE (Travel.trid = NEW.travel)))
  THEN
    SET NEW.location = NULL;

  END IF;
  END$$
DELIMITER ;


# Mimics Check Constraints on Activity since MySQL does not support them
DELIMITER $$
CREATE TRIGGER before_update_activity_trigger BEFORE UPDATE ON Activity
  FOR EACH ROW 
  BEGIN

  # Cannot plan an activity in a location user will not be at
  IF (SELECT lzip FROM Location WHERE Location.lid = NEW.location) != 
	 (SELECT lzip FROM Location WHERE Location.lid = 
	    (SELECT destination FROM Travel WHERE Travel.trid = NEW.travel))
  THEN
    SET NEW.location = NULL;

  # Cannot plan an activity outside the bounds of the trip
  ELSEIF ((NEW.adate < (SELECT start_date FROM Trip WHERE (Trip.title = NEW.trip))) OR
		   (NEW.adate > (SELECT end_date FROM Trip WHERE (Trip.title = NEW.trip))))
  THEN
    SET NEW.location = NULL;

  # Cannot plan an activity before the travel event that brings user to location
  ELSEIF (NEW.atime < (SELECT eta FROM Travel WHERE (Travel.trid = NEW.travel)))
  THEN
    SET NEW.location = NULL;

  END IF;
  END$$
DELIMITER ;

######################################################################################
										
# Weak entity set to Trip, dominant entity set to Activity
CREATE TABLE Travel (trid CHAR(20) NOT NULL,
                     method VARCHAR(15) NOT NULL,
					 tdate DATE NOT NULL,
                     start_time TIME NOT NULL,
                     eta TIME NOT NULL,
					 trip CHAR(20) NOT NULL,
					 place CHAR(20) NOT NULL, # where travel event is beginning
                     destination CHAR(20) NOT NULL, # where travel event is ended
                     PRIMARY KEY (trid, trip),
                     FOREIGN KEY (trip) REFERENCES Trip (title)
                                             ON DELETE CASCADE
                                             ON UPDATE CASCADE,
                     FOREIGN KEY (destination) REFERENCES Location (lid)
                                             ON UPDATE CASCADE,
					 FOREIGN KEY (place) REFERENCES Location (lid)
                                             ON UPDATE CASCADE);



# Mimics Check Constraints, since MySQL does not support them
DELIMITER $$
CREATE TRIGGER before_insert_travel_trigger BEFORE INSERT ON Travel
  FOR EACH ROW 
  BEGIN

  # Cannot plan a travel event before/after trip is planned to start/end
  IF (NEW.tdate < (SELECT start_date FROM Trip WHERE (Trip.title = NEW.trip))) OR
	 (NEW.tdate > (SELECT end_date FROM Trip WHERE (Trip.title = NEW.trip)))
  THEN
    SET NEW.trid = NULL;

  # Cannot start in one place and end in the same place
  ELSEIF (NEW.place = NEW.destination)
  THEN
    SET NEW.trid = NULL;

  END IF;
  END$$
DELIMITER ;

# Mimics Check Constraints, since MySQL does not support them
DELIMITER $$
CREATE TRIGGER before_update_travel_trigger BEFORE UPDATE ON Travel
  FOR EACH ROW 
  BEGIN

  # Cannot plan a travel event before/after trip is planned to start/end
  IF (NEW.tdate < (SELECT start_date FROM Trip WHERE (Trip.title = NEW.trip))) OR
	 (NEW.tdate > (SELECT end_date FROM Trip WHERE (Trip.title = NEW.trip)))
  THEN
    SET NEW.trid = NULL;

  # Cannot start in one place and end in the same place
  ELSEIF (NEW.place = NEW.destination)
  THEN
    SET NEW.trid = NULL;

  END IF;
  END$$
DELIMITER ;



