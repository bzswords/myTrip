# Bryan Swords
#!/usr/bin/python

import Tkinter as Tk
import ttk as tk
import MySQLdb as ms
import tkMessageBox
from pubsub import pub

"""
   Source code for myTrip. 
"""

###########################################################################
##############################           ##################################
#                         Information Viewers                             #
##############################           ##################################
###########################################################################

class viewLocationInfo(Tk.Toplevel):
   """
      Displays info stored about selected travel event
   """
   
   #///////////////////////////////////////////
   def __init__(self, lid, trip_name, trid):
      Tk.Toplevel.__init__(self)
      self.geometry("315x150+300+300") 
      self.title("Location Info")  
      self.configure(bg="blue")
      self.lid = lid
      self.trip_name = trip_name
      self.trid = trid
      
      #places all widgets on window
      self.placement()
   #///////////////////////////////////////////
   
   #---------------------------------------------------------------------
   
   def onClose(self):
      """ closes frame and returns to schedule """
      
      self.destroy()
      addActivity = AddActivity(self.trip_name, self.trid)
      
   #----------------------------------------------------------------------
   
   def placement(self):
      """ places widgets on frame """
      
      # all widgets exist on this
      bigframe = Tk.Frame(self, borderwidth=5, bg = 'cyan', relief=Tk.RAISED)
      bigframe.place(x=15, y=10)
      
      lid_lbl = Tk.Label(bigframe, text="LID:", bg='cyan')
      lidinfo = Tk.Label(bigframe, text=self.lid)
      name_lbl = Tk.Label(bigframe, text="Name: ", bg='cyan')
      street_lbl = Tk.Label(bigframe, text="Street: ", bg='cyan')
      address_lbl = Tk.Label(bigframe, text="Address: ", bg='cyan')
      
      db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
      cursor = db.cursor()
      
      # name
      cursor.execute("SELECT lname FROM Location \
                     WHERE Location.lid = %s", (self.lid))
      from_lid = cursor.fetchall()[0]
      fname = Tk.Label(bigframe, text=from_lid, bg='cyan')
      
      #street
      cursor.execute("SELECT street FROM Location WHERE \
                      Location.lid=%s", (self.lid))
      streetinfo = cursor.fetchall()
      locstreet = Tk.Label(bigframe, text=streetinfo[0], bg= 'cyan')
      
      # address
      cursor.execute("SELECT zip, city, country, state FROM \
                     Address WHERE Address.zip = (SELECT \
                     lzip from Location WHERE Location.lid=%s)", (self.lid))
      locadd = cursor.fetchall()
      ladd = Tk.Label(bigframe, text=locadd[0], bg='cyan')
      cursor.close()
      db.close()
      
      # placement
      lid_lbl.grid(column=0, row=0)
      lidinfo.grid(column=1, row=0)
      name_lbl.grid(column=0, row=1)
      fname.grid(column=1, row=1)
      street_lbl.grid(column=0, row=2)
      locstreet.grid(column=1, row=2)
      address_lbl.grid(column=0, row=3)
      ladd.grid(column=1, row=3)
      
      # back to Schedule
      backbutton = Tk.Button(bigframe, text="Back", command=self.onClose)
      backbutton.grid(column=1, row=4)


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class viewTravelInfo(Tk.Toplevel):
   """
      Displays info stored about selected travel event
   """
   
   #///////////////////////////////////////////
   def __init__(self, trip_name, trid):
      Tk.Toplevel.__init__(self)
      self.geometry("480x270+270+300") 
      self.title("Travel Info")  
      self.configure(bg="blue")
      self.trip_name = trip_name
      self.trid = trid
      
      #places all widgets on window
      self.placement()
   #///////////////////////////////////////////
   
   #---------------------------------------------------------------------
   
   def onClose(self):
      """ closes frame and returns to schedule """
      
      self.destroy()
      schedule = Schedule(self.trip_name)
      
   #----------------------------------------------------------------------
   
   def placement(self):
      """ places widgets on frame """
      
      bigframe = Tk.Frame(self, borderwidth=5, bg = 'cyan', relief=Tk.RAISED)
      bigframe.place(x=5, y=20)
      
      trip_name_lbl = Tk.Label(bigframe, text="Trip:", bg='cyan')
      tname = Tk.Label(bigframe, text=self.trip_name, bg='cyan')
      t_date = Tk.Label(bigframe, text="Date: ", bg='cyan')
      from_lbl = Tk.Label(bigframe, text="From: ", bg='cyan')
      to_lbl = Tk.Label(bigframe, text="To: ", bg='cyan')
      method_lbl = Tk.Label(bigframe, text="Method: ", bg='cyan')
      start_lbl = Tk.Label(bigframe, text="Start Time: ", bg='cyan')
      eta_lbl = Tk.Label(bigframe, text="ETA: ", bg='cyan')
      
      db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
      cursor = db.cursor()
      
      #date
      cursor.execute("SELECT tdate FROM Travel \
                     WHERE Travel.trid=%s", (self.trid[0]))
      traveldate = cursor.fetchall()
      tdate = Tk.Label(bigframe, text=traveldate[0], bg='cyan')
      # from
      cursor.execute("SELECT place FROM Travel \
                     WHERE Travel.trid = %s", (self.trid[0]))
      from_lid = cursor.fetchall()
      cursor.execute("SELECT lname, street FROM Location \
                     INNER JOIN Address ON Location.lzip = Address.zip \
                     WHERE Location.lid = %s", (from_lid[0]))
      from_name = cursor.fetchall()[0]
      fname = Tk.Label(bigframe, text=from_name[0] + " " + from_name[1], bg='cyan')
      
      #fromaddress
      cursor.execute("SELECT zip, city, country, state FROM Location \
                     INNER JOIN Address ON Location.lzip = Address.zip \
                     WHERE Location.lid = %s", (from_lid[0]))
      from_add = cursor.fetchall()
      fadd = Tk.Label(bigframe, text=from_add[0], bg= 'cyan')
      
      # to
      cursor.execute("SELECT destination FROM Travel \
                      WHERE Travel.trid=%s", (self.trid[0]))
      dest_lid = cursor.fetchall()
      cursor.execute("SELECT lname, street FROM Location \
                     INNER JOIN Address ON Location.lzip = Address.zip \
                     WHERE Location.lid = %s", (dest_lid[0]))
      dest_name = cursor.fetchall()
      dname = Tk.Label(bigframe, text=dest_name[0], bg='cyan')
      
      #toaddress
      cursor.execute("SELECT zip, city, country, state FROM Location \
                     INNER JOIN Address ON Location.lzip = Address.zip \
                     WHERE Location.lid = %s", (dest_lid[0]))
      to_add = cursor.fetchall()
      tadd = Tk.Label(bigframe, text=to_add[0], bg='cyan')
      
      # method
      cursor.execute("SELECT method FROM Travel WHERE \
                     Travel.trid=%s", (self.trid[0]))
      method = cursor.fetchall()
      mlbl = Tk.Label(bigframe, text=method[0], bg='cyan')
      
      # start time
      cursor.execute("SELECT start_time FROM Travel WHERE \
                              Travel.trid=%s", (self.trid[0]))
      start = cursor.fetchall()
      slbl = Tk.Label(bigframe, text=start[0], bg='cyan')
      
      # ETA
      cursor.execute("SELECT eta FROM Travel WHERE \
                            Travel.trid=%s", (self.trid[0]))
      eta = cursor.fetchall()
      cursor.close()
      db.close()
      elbl = Tk.Label(bigframe, text=eta[0], bg='cyan')
      
      # placement
      trip_name_lbl.grid(column=0, row=0)
      tname.grid(column=1, row=0)
      from_lbl.grid(column=0, row=1)
      fname.grid(column=1, row=1)
      fadd.grid(column=1, row=2)
      to_lbl.grid(column=0, row=3)
      dname.grid(column=1, row=3)
      tadd.grid(column=1, row=4)
      method_lbl.grid(column=0, row=5)
      mlbl.grid(column=1, row=5)
      start_lbl.grid(column=0, row=6)
      slbl.grid(column=1, row=6)
      eta_lbl.grid(column=0, row=7)
      elbl.grid(column=1, row=7)
      t_date.grid(column=0, row=8)
      tdate.grid(column=1, row=8)
      
      # back to Schedule
      backbutton = Tk.Button(bigframe, text="Back", command=self.onClose)
      backbutton.grid(column=1, row=9)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class viewActivityInfo(Tk.Toplevel):
   """
      Displays info stored about selected activity
   """
   
   #///////////////////////////////////////////
   def __init__(self, trip_name, trid, actname):
      Tk.Toplevel.__init__(self)
      self.geometry("500x180+300+300") 
      self.title("Activity Info")
      self.configure(bg="blue")  
      self.trip_name = trip_name
      self.trid = trid
      self.actname = actname
      
      #places all widgets on window
      self.placement()
   #///////////////////////////////////////////
   
   #---------------------------------------------------------------------
   
   def onClose(self):
      """ closes frame and returns to schedule """
      
      self.destroy()
      schedule = Schedule(self.trip_name)
      
   #----------------------------------------------------------------------
   
   def placement(self):
      """ places widgets on frame """
      
      bigframe = Tk.Frame(self, borderwidth=5, bg = 'cyan', relief=Tk.RAISED)
      bigframe.place(x=5, y=20)
      
      trip_name_lbl = Tk.Label(bigframe, text="Trip:", bg='cyan')
      tname = Tk.Label(bigframe, text=self.trip_name, bg='cyan')
      aname = Tk.Label(bigframe, text=self.actname[0], bg='cyan')
      descr_lbl = Tk.Label(bigframe, text="Description: ", bg='cyan')
      time_lbl = Tk.Label(bigframe, text="When: ", bg='cyan')
      where_lbl = Tk.Label(bigframe, text="Where: ", bg='cyan')
      
      db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
      cursor = db.cursor()
      
      # description
      cursor.execute("SELECT descr FROM Activity \
                     WHERE Activity.travel = %s \
                     AND Activity.aname = %s", (self.trid[0], self.actname))
      descr = cursor.fetchall()[0]
      descrlbl = Tk.Label(bigframe, text=descr[0], bg='cyan')
      
      #time
      cursor.execute("SELECT atime FROM Activity \
                     WHERE Activity.travel = %s AND\
                     Activity.descr=%s", (self.trid[0], descr[0]))
      time = cursor.fetchall()
      timelbl = Tk.Label(bigframe, text=time[0], bg= 'cyan')
      
      # where
      cursor.execute("SELECT location FROM Activity \
                      WHERE Activity.travel=%s AND\
                      Activity.descr=%s", (self.trid[0], descr[0]))
      where_lid = cursor.fetchall()
      cursor.execute("SELECT lname, street FROM Location \
                     INNER JOIN Address ON Location.lzip = Address.zip \
                     WHERE Location.lid = %s", (where_lid[0]))
      where_name = cursor.fetchall()[0]
      wname = Tk.Label(bigframe, text=where_name[0] + " " + where_name[1], bg='cyan')
      
      #whereaddress
      cursor.execute("SELECT zip, city, country, state FROM Location \
                     INNER JOIN Address ON Location.lzip = Address.zip \
                     WHERE Location.lid = %s", (where_lid[0]))
      where_add = cursor.fetchall()
      wadd = Tk.Label(bigframe, text=where_add[0], bg='cyan')
      cursor.close()
      db.close()
      
      # placement
      trip_name_lbl.grid(column=0, row=0)
      tname.grid(column=1, row=0)
      descr_lbl.grid(column=0, row=1)
      descrlbl.grid(column=1, row=1)
      time_lbl.grid(column=0, row=2)
      timelbl.grid(column=1, row=2)
      where_lbl.grid(column=0, row=3)
      wname.grid(column=1, row=3)
      wadd.grid(column=1, row=4)
      
      # back to Schedule
      backbutton = Tk.Button(bigframe, text="Back", command=self.onClose)
      backbutton.grid(column=1, row=8)
      
###########################################################################
##############################           ##################################
#                              Add Pages                                  #
##############################           ##################################
###########################################################################

class AddTravel(Tk.Toplevel):
   """ 
      Presents form to insert travel event
   """
   
   #///////////////////////////////////////////
   def __init__(self, trip_name):
      Tk.Toplevel.__init__(self)
      self.geometry("325x270+300+300")
      self.title("Add Travel")
      self.configure(bg="goldenrod")
      self.trip_name = trip_name
      
      #places all widgets
      self.placement()
   #///////////////////////////////////////////
   
   #-----------------------------------------------------------------------
   
   def onClose(self):
      """ brings user back to schedule """
      
      self.destroy()
      schedule = Schedule(self.trip_name)
   
   #------------------------------------------------------------------------
   
   def placement(self):
      """ places all widgets on window"""
      
      def NewTravel():
        """ finalizes entry to database """
        
        global travel_trid, travel_method, travel_date, travel_stime 
        global travel_eta, travel_place, travel_destination, cursor
         
        trid = travel_trid.get()
        method = travel_method.get()
        date = travel_date.get()
        stime = travel_stime.get()
        eta = travel_eta.get()
        place = travel_place.get()
        destination = travel_destination.get() 
        
        # database connection and interaction
        db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
        cursor = db.cursor()
        cursor.execute("INSERT INTO Travel (trid, method, \
                       tdate, start_time, eta, trip, place, destination) \
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", 
                       (trid, method, date, stime, eta, self.trip_name[0], place, destination))
        cursor.close()
        db.commit()
        db.close()
        print "Successful Insert"
        tkMessageBox.showinfo("Success", "Added your new travel event: " + trid)
        return
      
      # frame all widgets will be on     
      bigframe = Tk.Frame(self, borderwidth=5, bg = 'yellow', relief=Tk.RAISED)
      bigframe.place(x=5, y=20)
      
      # entry labels
      trid_lbl = Tk.Label(bigframe, text="TRID: ", bg='yellow')
      method_lbl = Tk.Label(bigframe, text="Method: ", bg='yellow')
      date_lbl = Tk.Label(bigframe, text="Date: ", bg='yellow')
      stime_lbl = Tk.Label(bigframe, text="Start Time: ", bg='yellow')
      eta_lbl = Tk.Label(bigframe, text="ETA: ", bg= 'yellow')
      dfrom_lbl = Tk.Label(bigframe, text="Depart From: ", bg='yellow')
      destination_lbl = Tk.Label(bigframe, text="Destination: ", bg='yellow')
      
      # entry boxes
      trid_entry = Tk.Entry(bigframe, width=25, textvariable=travel_trid)
      method_entry = Tk.Entry(bigframe, width=25, textvariable=travel_method)
      date_entry = Tk.Entry(bigframe, width=25, textvariable=travel_date)
      stime_entry = Tk.Entry(bigframe, width=25, textvariable=travel_stime)
      eta_entry = Tk.Entry(bigframe, width=25, textvariable=travel_eta)
      dfrom_entry = Tk.Entry(bigframe, width=25, textvariable=travel_place)
      destination_entry = Tk.Entry(bigframe, width=25, textvariable=travel_destination)
      
      # placement of widgets
      trid_lbl.grid(column=0, row=0)
      trid_entry.grid(column=1, row=0)
      method_lbl.grid(column=0, row=1)
      method_entry.grid(column=1, row=1)
      date_lbl.grid(column=0, row=2)
      date_entry.grid(column=1, row=2)
      stime_lbl.grid(column=0, row=3)
      stime_entry.grid(column=1, row=3)
      eta_lbl.grid(column=0, row=4)
      eta_entry.grid(column=1, row=4)
      dfrom_lbl.grid(column=0, row=5)
      dfrom_entry.grid(column=1, row=5)
      destination_lbl.grid(column=0, row=6)
      destination_entry.grid(column=1, row=6)
      
      backbutton = Tk.Button(bigframe, text="Back", command=self.onClose)
      backbutton.grid(column=0, row=7)
      addbutton = Tk.Button(bigframe, text="Add Travel", command=NewTravel)
      addbutton.grid(column=1, row=7)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class AddLocation(Tk.Toplevel):
   """ 
      Presents form to insert new location
   """
   
   #///////////////////////////////////////////
   def __init__(self, trip_name, trid):
      Tk.Toplevel.__init__(self)
      self.geometry("300x268+300+300")
      self.title("Add Location")
      self.configure(bg='goldenrod')
      self.trip_name = trip_name
      self.trid = trid
      
      #places all widgets
      self.placement()
   #///////////////////////////////////////////
   
   #-----------------------------------------------------------------------
   
   def onClose(self):
      """ brings user back to AddActivity """
      
      self.destroy()
      addActivity = AddActivity(self.trip_name, self.trid)
   
   #------------------------------------------------------------------------
   
   def placement(self):
      """ places all widgets on window"""
      
      def NewLocation():
        """ finalizes insert into database """
         
        global loc_lid, loc_name, loc_street 
        global loc_zip, loc_city, loc_country, loc_state, cursor
         
        lid = loc_lid.get()
        name = loc_name.get()
        street = loc_street.get()
        zip = loc_zip.get()
        city = loc_city.get()
        country = loc_country.get()
        state = loc_state.get() 
        
        # connection and interaction with database
        db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
        cursor = db.cursor()
        cursor.execute("SELECT count(*) FROM Address WHERE \
                       Address.zip=%s", (zip))
        zipexists = cursor.fetchall()
        if (zipexists[0] > 0): # if > 1 it does not need to be stored in Address again
           cursor.execute("INSERT INTO Location (lid, lname, street, lzip) \
                          VALUES(%s, %s, %s, %s)", (lid, name, street, zip))
           cursor.close
           db.commit()
           db.close()
           print "Successful Insert"
           tkMessageBox.showinfo("Success", "Added your new Location: " + name)
           return
        else:
           cursor.execute("INSERT INTO Address (zip, city, country, state) \
                          VALUES (%s, %s, %s, %s)", (zip, city, country, state))
           cursor.execute("INSERT INTO Location (lid, lname, street, lzip) \
                          VALUES (%s, %s, %s, %s)", (lid, name, street, zip))
           cursor.close()
           db.commit()
           db.close()
           print "Successful Insert"
           tkMessageBox.showinfo("Success", "Added your new Location: " + name)
           return
      
      # frame all widgets exist on     
      bigframe = Tk.Frame(self, borderwidth=5, bg = 'yellow', relief=Tk.RAISED)
      bigframe.place(x=5, y=20)
      
      # entry labels
      lid_lbl = Tk.Label(bigframe, text="LID: ", bg='yellow')
      lname_lbl = Tk.Label(bigframe, text="Name: ", bg='yellow')
      street_lbl = Tk.Label(bigframe, text="Street: ", bg='yellow')
      zip_lbl = Tk.Label(bigframe, text="Zip: ", bg='yellow')
      city_lbl = Tk.Label(bigframe, text="City: ", bg='yellow')
      country_lbl = Tk.Label(bigframe, text="Country: ", bg='yellow')
      state_lbl = Tk.Label(bigframe, text="State: ", bg='yellow')
      
      # entry forms
      lid_entry = Tk.Entry(bigframe, width=25, textvariable=loc_lid)
      lname_entry = Tk.Entry(bigframe, width=25, textvariable=loc_name)
      street_entry = Tk.Entry(bigframe, width=25, textvariable=loc_street)
      zip_entry = Tk.Entry(bigframe, width=25, textvariable=loc_zip)
      city_entry = Tk.Entry(bigframe, width=25, textvariable=loc_city)
      country_entry = Tk.Entry(bigframe, width=25, textvariable=loc_country)
      state_entry = Tk.Entry(bigframe, width=25, textvariable=loc_state)
      
      # placement of widgets 
      lid_lbl.grid(column=0, row=0)
      lid_entry.grid(column=1, row=0)
      lname_lbl.grid(column=0, row=1)
      lname_entry.grid(column=1, row=1)
      street_lbl.grid(column=0, row=2)
      street_entry.grid(column=1, row=2)
      zip_lbl.grid(column=0, row=3)
      zip_entry.grid(column=1, row=3)
      city_lbl.grid(column=0, row=4)
      city_entry.grid(column=1, row=4)
      country_lbl.grid(column=0, row=5)
      country_entry.grid(column=1, row=5)
      state_lbl.grid(column=0, row=6)
      state_entry.grid(column=1, row=6)
      
      # buttons with actions
      backbutton = Tk.Button(bigframe, text="Back", command=self.onClose)
      backbutton.grid(column=0, row=7)
      addbutton = Tk.Button(bigframe, text="Add Location", command=NewLocation)
      addbutton.grid(column=1, row=7)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class AddActivity(Tk.Toplevel):
   """ 
      Displays form to INSERT activity into myTrip database
      Listbox on side lists all known locations in area. Option 
      to add new locations brings you to new form.
   """
   #///////////////////////////////////////////
   def __init__(self, trip_name, trid):
      Tk.Toplevel.__init__(self)
      self.geometry("570x300+300+300")
      self.title("Add Activity")
      self.configure(bg="blue")
      self.trip_name = trip_name
      self.trid = trid
      
      # places widgets on frame
      self.placement()
   #////////////////////////////////////////////
      
   #----------------------------------------------------------------------
   
   def onClose(self):
       """ closes the frame and returns to schedule """
       
       self.destroy()
       schedule = Schedule(self.trip_name)
       
   #----------------------------------------------------------------------
   
   def toViewLocation(self, loc):
       """ closes the frame and returns to schedule """
       
       self.destroy()
       viewlocinfo = viewLocationInfo(loc, self.trip_name, self.trid)
       
   #-----------------------------------------------------------------------
   
   def NewLocation(self):
      """ brings user to window to add new location """
      
      self.destroy()
      addLocation = AddLocation(self.trip_name, self.trid)
   
   #-----------------------------------------------------------------------
      
        
   def placement(self):
      """ places widgets on frame """
      
      def viewInfo():
         """ """
         
         index = listb.curselection()[0]
         location = listb.get(index)
         print self.trid[0], location
         
         db = ms.connect(host="localhost", user="root", 
                         passwd="tactics1234", db="myTrip")
         cursor = db.cursor()
         cursor.execute("SELECT lid FROM Location WHERE Location.lname = %s \
                        AND Location.lzip = (SELECT lzip FROM Location \
                        WHERE Location.lid = (SELECT destination FROM \
                        Travel WHERE Travel.trid = %s))", (location, self.trid[0]))
         lid = cursor.fetchall()[0]
         print lid
         cursor.close()
         db.close()
         
         self.toViewLocation(lid)
         
      
      def deleteLocation():
        """ """
          
        # gets aname from listbox, deletes from listbox 
        index = listb.curselection()[0]
        location = listb.get(index)
        print location
        listb.delete(index)
          
        # Database Connection
        db = ms.connect(host="localhost", user="root", 
                        passwd="tactics1234", db="myTrip")
        cursor = db.cursor()
        cursor.execute("SELECT lzip FROM Location WHERE \
                       Location.lid=(SELECT destination FROM Travel WHERE \
                       Travel.trid=%s)", (self.trid[0]))
        zip = cursor.fetchall()[0]
        print zip[0]
        cursor.execute("DELETE FROM Location WHERE \
                       (Location.lname=%s) AND \
                       (Location.lzip = %s)", (location, zip[0]))
        cursor.close()
        db.commit()
        db.close()
        print "Deleted"
      
      def NewActivity():
         """ 
         shows message box saying if it was a success or failure 
         INSERTS into the database
         """
      
         index = listb.curselection()[0]
         loc = listb.get(index)
         destination = dest[0]
         
         print loc, destination[0]
      
         global act_n, act_d, act_da, act_t, conn
         name = act_n.get()
         descr = act_d.get()
         date = act_da.get()
         time = act_t.get()
         # get location
         db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
         cursor = db.cursor()
         cursor.execute("SELECT lid FROM Location WHERE \
                         Location.lname=%s AND Location.lzip=%s", (loc, destination[0]))
         lid = cursor.fetchall()[0]
         print lid[0]
      
         if name == "" or descr == "" or date == "" or time == "" :
            tkMessageBox.showerror("Bad Data", "Some Or All Required Fields Are Blank")
            return
         else:
            cursor.execute("INSERT INTO Activity \
                           (aname, descr, adate, atime, trip, location, travel) \
                           VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                           (name, descr, date, time, self.trip_name[0], lid[0], self.trid[0]))
         cursor.close()
         db.commit()
         db.close
         print "Successful Insert"
         tkMessageBox.showinfo("Success", "Added your new activity: " + name)
         return
      
      # frame entry widgets exist on
      entryframe = Tk.Frame(self, borderwidth=5, bg = 'cyan', relief=Tk.RAISED)
      entryframe.place(x=7, y=50)
      
      # creates listbox with locations
      lframe = Tk.Frame(self, borderwidth=5, bg = 'cyan', relief=Tk.RAISED)
      scrollbar = Tk.Scrollbar(lframe, orient=Tk.VERTICAL)
      listb = Tk.Listbox(lframe, yscrollcommand=scrollbar.set)
      scrollbar.config(command=listb.yview)
      scrollbar.grid(row=0, column=1, sticky=Tk.N+Tk.S)
      listb.grid(row=0, column=0)
      lframe.place(x=375, y=10)
      
      # places items in listbox
      db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
      cursor = db.cursor()
      cursor.execute("SELECT lzip FROM Location WHERE Location.lid = \
                     (SELECT destination FROM Travel WHERE \
                     Travel.trid=%s)", (self.trid[0]))
      dest = cursor.fetchall()
      cursor.execute("SELECT lname FROM Location WHERE Location.lzip=%s", (dest[0]))
      data = cursor.fetchall()
      for row in data:
        listb.insert(Tk.END, row[0])
      cursor.close()
      db.close()
      
      # labels for each entry
      lbl_name = Tk.Label(entryframe, text="Name: ", bg = 'cyan')
      lbl_desc = Tk.Label(entryframe, text="Description:", bg = 'cyan')
      lbl_date = Tk.Label(entryframe, text="Date: (YYYY-DD-MM)", bg = 'cyan')
      lbl_time = Tk.Label(entryframe, text="Time: (HH:MM:SS)", bg = 'cyan')
       
      # widgets for data entry
      aname = Tk.Entry(entryframe, width = 25, textvariable=act_n)
      desc = Tk.Entry(entryframe, width = 25, textvariable=act_d)
      adate = Tk.Entry(entryframe, width = 25, textvariable=act_da) 
      atime = Tk.Entry(entryframe, width= 25, textvariable=act_t)
      
      # Buttons
      addbutton = Tk.Button(entryframe, text = "Add Activity", command = NewActivity)
      backbutton = Tk.Button(entryframe, text = "Back", command = self.onClose)
      locationsbutton = Tk.Button(lframe, text="Add Location", command=self.NewLocation)
      deletelocation = Tk.Button(lframe, text="Delete Location", command=deleteLocation)
      locinfo = Tk.Button(lframe,text="Location Info", command=viewInfo)
       
      #Place widgets
      lbl_name.grid(column=0, row=0)
      aname.grid(column=1, row=0)
      lbl_desc.grid(column=0, row=1)
      desc.grid(column=1, row=1)
      lbl_date.grid(column=0, row=2)
      adate.grid(column=1, row=2)
      lbl_time.grid(column=0, row=3)
      atime.grid(column=1,row=3)
      addbutton.grid(column=0, row=4)
      backbutton.grid(column=1, row=4)
      locinfo.grid(column=0, row=1)
      locationsbutton.grid(column=0, row=2)
      deletelocation.grid(column=0, row=3)
      
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class AddTrip(Tk.Toplevel):
   """
      Presents form to INSERT new Trip 
   """
   
   #////////////////////////////////////
   def __init__(self):
      Tk.Toplevel.__init__(self)
      self.geometry("400x170+300+300")
      self.title("Add Trip")
      self.configure(bg="goldenrod")
      
      # places widgets on frame
      self.placement()
   #////////////////////////////////////
      
   #----------------------------------------------------------------------
   
   def onClose(self):
       """ closes the frame and sends a message to the main frame """
       
       self.destroy()
       pub.sendMessage("backToBeginning", arg1="data")
   
   #-----------------------------------------------------------------------
      
   def NewTrip(self):
      """ 
      INSERT new trip into database
      """
      global add_t, add_s, add_e, cursor
      title = add_t.get()
      start = add_s.get()
      end = add_e.get()
      
      
      if title == "" or start == "" or end == "" :
         tkMessageBox.showerror("Bad Data", "Some Or All Required Fields Are Blank")
         return
      else:
         db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
         cursor = db.cursor()
         cursor.execute("INSERT INTO Trip \
                        (title, start_date, end_date) \
                        VALUES (%s, %s, %s)", (title, start, end))
         cursor.close()
         db.commit()
         db.close
         print "Successful Insert"
         tkMessageBox.showinfo("Success", "Added your new trip: " + title)
         return
           
   #-----------------------------------------------------------------------
        
   def placement(self):
      """ places widgets on frame """
      
      # frame all widgets will exist in
      bigframe = Tk.Frame(self, borderwidth=5, bg = 'yellow', relief=Tk.RAISED)
      bigframe.place(x=2, y=20)
      
      # labels for each entry
      lbl_t = Tk.Label(bigframe, text="Title:", bg='yellow')
      lbl_s = Tk.Label(bigframe, text="Start Date: (YYYY-MM-DD)", bg='yellow')
      lbl_e = Tk.Label(bigframe, text="End Date: (YYYY-MM-DD)", bg='yellow')
       
      # widgets for data entry
      title = Tk.Entry(bigframe, width = 25, textvariable=add_t)
      start_date = Tk.Entry(bigframe, width = 25, textvariable=add_s) 
      end_date = Tk.Entry(bigframe, width = 25, textvariable=add_e) 
      addbutton = Tk.Button(bigframe, text = "Add Trip", command = self.NewTrip)
      backbutton = Tk.Button(bigframe, text = "Back", command = self.onClose)
       
      #Place widgets
      lbl_t.grid(column=1, row=4)
      title.grid(column=2, row=4)
      lbl_s.grid(column=1, row=5)
      start_date.grid(column=2, row=5)
      lbl_e.grid(column=1, row=6)
      end_date.grid(column=2, row=6)
      addbutton.grid(column=1, row=7)
      backbutton.grid(column=2, row=7)

###########################################################################
##############################           ##################################
#                               Schedule                                  #
##############################           ##################################
###########################################################################

class Schedule(Tk.Toplevel):
   """ 
      Displays Travel and Activity info. Gives options to delete and add info of both
   """
   #////////////////////////////////////////
   def __init__(self, trip_name):
      Tk.Toplevel.__init__(self)
      self.geometry("375x375+300+300")
      self.title("Schedule")
      self.configure(bg='goldenrod')
      self.trip_name = trip_name
      
      # places widgets on frame
      self.placement()
   #/////////////////////////////////////////
       
   #----------------------------------------------------------------------
   
   def onClose(self):
      """ closes the frame and sends a message to the main frame """
      
      self.destroy()
      pub.sendMessage("backToBeginning", arg1="data")
    
   #----------------------------------------------------------------------
   
   def openActivity(self, trid):
      """ opens add trip frame and hides main frame """
        
      self.destroy()
      addActivity = AddActivity(self.trip_name, trid)
            
   #----------------------------------------------------------------------
   
   def viewTravelInfo(self, trid):
      """ brings user to full travel info stored"""
      
      self.destroy()
      travelInfo = viewTravelInfo(self.trip_name, trid)
      
   #----------------------------------------------------------------------
   
   def viewActivityInfo(self, trid, actname):
      """ brings user to full activity info stored """
      
      self.destroy()
      activityInfo = viewActivityInfo(self.trip_name, trid, actname)
      
   #-----------------------------------------------------------------------
   
   def openTravel(self):
      """ brings user to form to add new travel event """
      
      self.destroy()
      addTravel = AddTravel(self.trip_name)
   
   #----------------------------------------------------------------------
   
   def placement(self):
      """ places all widgets on frame """
             
      def deleteTravel():
         """ deletes selected travel event from database """
          
         # gets trid from listbox, deletes from listbox 
         index = listbt.curselection()[0]
         travel_id = listbt.get(index)
         print travel_id
         listbt.delete(index)
         listbact.delete(0,Tk.END)
          
         # Database Connection
         db = ms.connect(host="localhost", user="root", 
                         passwd="tactics1234", db="myTrip")
         cursor = db.cursor()
         cursor.execute("DELETE FROM Travel WHERE (Travel.trid=%s)", (travel_id))
         cursor.close()
         db.commit()
         db.close()
         print "Deleted"
         
      def viewActivities():
         """ """
         index = listbt.curselection()[0]
         trid = listbt.get(index)
         
         listbact.delete(0,Tk.END)
         db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
         cursor = db.cursor()
         cursor.execute("SELECT aname FROM Activity \
                         WHERE Activity.travel = %s \
                         ORDER BY Activity.atime", (trid[0]))
         data = cursor.fetchall()
         for row in data:
           listbact.insert(Tk.END, row[0])
         cursor.close()
         db.close()
         
         def getActivityInfo():
            """ """
            index = listbact.curselection()[0]
            actname = listbact.get(index)
            print actname
            
            self.viewActivityInfo(trid, actname)
            
         def deleteActivity():
            """ """
            
            # gets aname from listbox, deletes from listbox 
            index = listbact.curselection()[0]
            activity = listbact.get(index)
            print activity
            listbact.delete(index)
          
            # Database Connection
            db = ms.connect(host="localhost", user="root", 
                            passwd="tactics1234", db="myTrip")
            cursor = db.cursor()
            cursor.execute("DELETE FROM Activity WHERE \
                           (Activity.aname=%s) AND \
                           (Activity.travel = %s)", (activity, trid[0]))
            cursor.close()
            db.commit()
            db.close()
            print "Deleted"
         
         activityinfo.configure(command=getActivityInfo)
         deleteactivity.configure(command=deleteActivity)
         
      def getAddInfo():
         """ gets trid and sends user to AddActivity """
         index = listbt.curselection()[0]
         trid = listbt.get(index)
         
         self.openActivity(trid)
         
      def getTravelInfo():
         """ gets trid and sends user to viewTravelInfo """
         index = listbt.curselection()[0]
         trid = listbt.get(index)
         
         self.viewTravelInfo(trid)
       
      # most widgets exist on this   
      bigframe = Tk.Frame(self, borderwidth=5, bg = 'yellow', relief=Tk.RAISED)
      bigframe.place(x=5, y=50)
      
      # trip dates exist on this
      dateframe = Tk.Frame(self, borderwidth=5, bg = 'yellow', relief=Tk.RAISED)
      dateframe.place(x=25, y=10)
      
      # Creates trip info labels
      tsdate = Tk.Label(dateframe, text="Start Date:", bg='yellow')
      tsdate.grid(column=0, row=0)
      tedate = Tk.Label(dateframe, text="End Date:", bg='yellow')
      tedate.grid(column=3, row=0)
      
      # places info in dateframe
      db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
      cursor = db.cursor()
      cursor.execute("SELECT start_date FROM Trip WHERE \
                    Trip.title = %s", (self.trip_name))
      startdate = cursor.fetchall()
      tstartdate = Tk.Label(dateframe, text=startdate, bg='yellow')
      tstartdate.grid(column=2, row=0)
      cursor.execute("SELECT end_date FROM Trip WHERE \
                    Trip.title = %s", (self.trip_name))
      enddate = cursor.fetchall()
      tenddate = Tk.Label(dateframe, text=enddate, bg='yellow')
      tenddate.grid(column=4, row=0)
      
      # Creates travel and activity labels
      travel_lbl = Tk.Label(bigframe, text="Travel", bg="yellow")
      travel_lbl.grid(column=1, row=0)
      activity_lbl = Tk.Label(bigframe, text="Activity", bg="yellow")
      activity_lbl.grid(column=4, row=0)
      
      # creates travel listbox with scrollbar  
      tframe = Tk.Frame(bigframe)
      scrollbart = Tk.Scrollbar(tframe, orient=Tk.VERTICAL)
      listbt = Tk.Listbox(tframe, yscrollcommand=scrollbart.set)
      scrollbart.config(command=listbt.yview)
      scrollbart.grid(row=0, column=1, sticky=Tk.N+Tk.S)
      listbt.grid(row=0, column=0)
      tframe.grid(column=1, row=3) 
      
      # creates activity listbox
      actframe = Tk.Frame(bigframe)
      scrollbaract = Tk.Scrollbar(actframe, orient=Tk.VERTICAL)
      listbact = Tk.Listbox(actframe, yscrollcommand=scrollbaract.set)
      scrollbaract.config(command=listbact.yview)
      scrollbaract.grid(row=0, column=1, sticky=Tk.N+Tk.S)
      listbact.grid(row=0, column=0)
      actframe.grid(column=4, row=3) 
      
      # places items in listbox
      db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
      cursor = db.cursor()
      cursor.execute("SELECT trid FROM Travel WHERE \
                     Travel.trip = %s ORDER BY Travel.tdate", (self.trip_name))
      data = cursor.fetchall()
      for row in data:
        listbt.insert(Tk.END, row)
      cursor.close()
      db.close()
      
      # Button to go to view activities
      activitybutton = Tk.Button(bigframe, text="Ok", command=viewActivities)
      activitybutton.grid(column=1, row=5)
      
      addActButton = Tk.Button(bigframe, text="Add Activity", command=getAddInfo)
      addActButton.grid(column=4,row=5)
      
      # Button to go to view travel info
      travelbutton = Tk.Button(bigframe, text="View Travel Info", command=getTravelInfo)
      travelbutton.grid(column=1, row=6)
      
      # Button to view activity info
      activityinfo = Tk.Button(bigframe, text="View Activity Info")
      activityinfo.grid(column=4, row=6)
      
      # Button to delete travel event
      deletetravel = Tk.Button(bigframe, text="Delete Travel", command=deleteTravel)
      deletetravel.grid(column=1, row=7)
      
      # Button to delete Activity
      deleteactivity = Tk.Button(bigframe, text="Delete Activity")
      deleteactivity.grid(column=4, row=7)
      
      # Button to go to AddTravel
      addTravelButton = Tk.Button(bigframe, text="Add Travel", command=self.openTravel)
      addTravelButton.grid(column=1, row=8)
      
      # Button to go back
      backbutton = Tk.Button(bigframe, text="Back", command=self.onClose)
      backbutton.grid(column=4, row=8)

###########################################################################
##############################           ##################################
#                                Update                                   #
##############################           ##################################
###########################################################################
                  
class UpdateTrip(Tk.Toplevel):
   """
      Presents form to UPDATE existing Trip. Be sure to click on a trip in the listbox
      before pressing update button
   """
   
   #////////////////////////////////////
   def __init__(self, trip):
      Tk.Toplevel.__init__(self)
      self.trip = trip
      self.geometry("400x130+300+300")
      self.title("Update Trip")
      self.configure(bg="goldenrod")
      
      # places widgets on frame
      self.placement()
   #////////////////////////////////////
      
   #----------------------------------------------------------------------
   
   def onClose(self):
       """ closes the frame and sends a message to the main frame """
       
       self.destroy()
       pub.sendMessage("backToBeginning", arg1="data")
   
   #-----------------------------------------------------------------------
      
   def EditTrip(self):
      """ 
      UPDATE trip. Cannot change name. Only can change start and end dates
      """
      global update_s, update_e, cursor
      start = update_s.get()
      end = update_e.get()
      
      if start == "" and end == "" :
         tkMessageBox.showerror("Bad Data", "Some Or All Required Fields Are Blank")
         return
      elif start != "" and end == "" :
         db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
         cursor = db.cursor()
         cursor.execute("UPDATE Trip SET Trip.start_date =%s WHERE \
                        Trip.title=%s", (start, self.trip[0]))
         cursor.close()
         db.commit()
         db.close()
         print "Successful Update"
         tkMessageBox.showinfo("Success", "Updated your trip: " + self.trip[0])
         return
      elif start == "" and end != "":
         db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
         cursor = db.cursor()
         cursor.execute("UPDATE Trip SET Trip.end_date =%s \
                        WHERE Trip.title=%s", (end, self.trip[0]))
         cursor.close()
         db.commit()
         db.close()
         print "Successful Update"
         tkMessageBox.showinfo("Success", "Updated your trip: " + self.trip[0])
         return
      else:
         db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
         cursor = db.cursor()
         cursor.execute("UPDATE Trip SET Trip.start_date=%s, \
                        Trip.end_date=%s WHERE Trip.title=%s", (start, end, self.trip[0]))
         cursor.close()
         db.commit()
         db.close
         print "Successful Update"
         tkMessageBox.showinfo("Success", "Updated your trip: " + self.trip[0])
         return
           
   #-----------------------------------------------------------------------
        
   def placement(self):
      """ places widgets on frame """
      
      # frame all widgets will exist in
      bigframe = Tk.Frame(self, borderwidth=5, bg = 'yellow', relief=Tk.RAISED)
      bigframe.place(x=2, y=20)
      
      # labels for each entry
      lbl_s = Tk.Label(bigframe, text="Start Date: (YYYY-MM-DD)", bg='yellow')
      lbl_e = Tk.Label(bigframe, text="End Date: (YYYY-MM-DD)", bg='yellow')
       
      # widgets for data entry
      start_date = Tk.Entry(bigframe, width = 25, textvariable=update_s) 
      end_date = Tk.Entry(bigframe, width = 25, textvariable=update_e) 
      updatebutton = Tk.Button(bigframe, text = "Update Trip", command = self.EditTrip)
      backbutton = Tk.Button(bigframe, text = "Back", command = self.onClose)
       
      #Place widgets
      lbl_s.grid(column=1, row=5)
      start_date.grid(column=2, row=5)
      lbl_e.grid(column=1, row=6)
      end_date.grid(column=2, row=6)
      updatebutton.grid(column=1, row=7)
      backbutton.grid(column=2, row=7)
    

###########################################################################
##############################           ##################################
#                                Main                                     #
##############################           ##################################
###########################################################################

class myTrip(object):
    """""
    First page shown when myTrip is opened. Allows you to add/delete/update a Trip
    
    """""
    #////////////////////////////////////////
    def __init__(self, parent):
       """ Constructor """
       self.root = parent
       self.root.title("myTrip")
       
       # listens for AddTrip, UpdateTrip, or Schedule to close
       pub.subscribe(self.listener, "backToBeginning")
       
       # places all widgets on frame
       self.placement()
    #/////////////////////////////////////////
          
    #----------------------------------------------------------------------
    
    def listener(self, arg1, arg2=None):
       """ pubsub listener - opens main frame when otherFrame closes """

       self.show()
       
    #----------------------------------------------------------------------
    
    def hide(self):
       """ hides main page """
    
       self.root.withdraw()
        
    #----------------------------------------------------------------------
    
    def openAddTrip(self):
        """ opens add trip frame and hides main frame """
        
        self.hide()
        addTrip = AddTrip()
        
    #----------------------------------------------------------------------
    
    def openUpdateTrip(self, trip_name):
        """ opens update trip frame and hides main frame """
        
        self.hide()
        updateTrip = UpdateTrip(trip_name)
    
    #----------------------------------------------------------------------
    
    def openSchedule(self, trip_name):
        """ opens schedule frame and hides main frame """
        
        self.hide()
        schedule = Schedule(trip_name)
            
    #-------------------------------------------------------------------------
    
    def show(self):
        """ shows main frame """
        
        self.placement()
        self.root.update()
        self.root.deiconify()
       
    #------------------------------------------------------------------------
          
    def placement(self): 
       """ Places widgets on screen """ 
       
       def deleteTrip():
          """ deletes selected trip from database """
          
          # gets trip_name from listbox, deletes from listbox 
          index = listb.curselection()[0]
          trip_name = listb.get(index)
          print trip_name[0]
          listb.delete(index)
          
          # Database Connection
          db = ms.connect(host="localhost", user="root", 
                          passwd="tactics1234", db="myTrip")
          cursor = db.cursor()
          cursor.execute("DELETE FROM Trip WHERE (Trip.title=%s)", (trip_name))
          cursor.close()
          db.commit()
          db.close()
          print "Deleted"
          
       def getUpdate():
          """ opens update trip window """
          
          # gets trip_name from listbox, deletes from listbox 
          index = listb.curselection()[0]
          trip_name = listb.get(index)
          
          self.openUpdateTrip(trip_name)
          
       def getSchedule():
          """ opens schedule """
          
          # gets trip_name from listbox, deletes from listbox 
          index = listb.curselection()[0]
          trip_name = listb.get(index)
          
          self.openSchedule(trip_name)

          
       # frame all widgets will exist in
       bigframe = Tk.Frame(root, borderwidth=5, bg = 'cyan', relief=Tk.RAISED)
       bigframe.place(x=5, y=15)
       
       myTrip_lbl = Tk.Label(bigframe, text="myTrip", 
                             fg="yellow", bg="cyan", font=("Helvetica", 24))
       myTrip_lbl.grid(row=0, column=1)
    
       # creates listbox 
       lframe = Tk.Frame(bigframe)
       scrollbar = Tk.Scrollbar(lframe, orient=Tk.VERTICAL)
       listb = Tk.Listbox(lframe, yscrollcommand=scrollbar.set)
       scrollbar.config(command=listb.yview)
       scrollbar.grid(row=0, column=1, sticky=Tk.N+Tk.S)
       listb.grid(row=0, column=0)
       lframe.grid(column=1, row=3)

       # places items in listbox
       db = ms.connect(host="localhost", user="root", passwd="tactics1234", db="myTrip")
       cursor = db.cursor()
       cursor.execute("SELECT title FROM Trip")
       data = cursor.fetchall()[0]
       for row in data:
          listb.insert(Tk.END, row)
       cursor.close()
       db.close()
      
       # Button to go to AddTrip
       tripbutton = Tk.Button(bigframe, text="Add New Trip", command=self.openAddTrip)
       tripbutton.grid(column=1, row=8)
       
       # Deletes Trip from database
       deletebutton = Tk.Button(bigframe, text="Delete Trip", command=deleteTrip)
       deletebutton.grid(column=0, row=8)
       
       # Button to go to Update
       updatebutton = Tk.Button(bigframe, text="Update Trip", command=getUpdate)
       updatebutton.grid(column=5, row=8)
       
       # Button to go to Schedule
       schedbutton = Tk.Button(bigframe, text="Ok", command=getSchedule)
       schedbutton.grid(column=1, row=9)
    
#+++++++++++++++++++++++++++++++++++++++++


if __name__ == "__main__":  
   root = Tk.Tk()         
   app = myTrip(root)
   root.geometry("400x300+300+300")
   root.configure(bg="blue")
   
   # Global Variables used by widgets
   # Tkinter widgets need these to return values
   add_t = Tk.StringVar() # Add Trip Title
   add_s = Tk.StringVar() # Add Trip Start_date
   add_e = Tk.StringVar() # Add Trip End_date
   
   update_t = Tk.StringVar() # Update Trip Title
   update_s = Tk.StringVar() # Update Trip Start_date
   update_e = Tk.StringVar() # Update Trip End_date
   
   travel_trid = Tk.StringVar() # Add Travel Trid
   travel_method = Tk.StringVar() # Add Travel Method
   travel_date = Tk.StringVar() # Add Travel Date
   travel_stime = Tk.StringVar() # Add Travel Start Time
   travel_eta = Tk.StringVar() # Add Travel ETA
   travel_place = Tk.StringVar() # Add Travel Place
   travel_destination = Tk.StringVar() # Add Travel Destination
   
   act_n = Tk.StringVar() # Add Activity Name
   act_d = Tk.StringVar() # Add Activity Description
   act_da = Tk.StringVar() # Add Activity Date
   act_t = Tk.StringVar() # Add Activity Time
   
   loc_lid = Tk.StringVar() # Add Location Lid
   loc_name = Tk.StringVar() # Add Location Name
   loc_street = Tk.StringVar() # Add Location Street
   loc_zip = Tk.StringVar() # Add Location Zip
   loc_city = Tk.StringVar() # Add Location City
   loc_country = Tk.StringVar() # Add Location Country
   loc_state = Tk.StringVar() # Add Location State

   root.mainloop()
   
