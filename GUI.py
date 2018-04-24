'''
Created on 12 Apr 2018

@author: westj
'''
from PIL import Image, ImageTk
import tkinter as tk
import os.path
from tkinter import font
from tkinter import messagebox

class GUI():

    def __init__(self):   

        self.window = tk.Tk()
        self.window.columnconfigure(0, weight=1)
        self.window.columnconfigure(1, weight=6)
        self.window.rowconfigure(1, weight=1)
        self.window.config()
        self.window.minsize(700, 400)

        self.build(self.window)
        self.window.mainloop()
            
    def build(self, master):
        """
        Author:     Jacob West
        Date:       18/04/2018
        Purpose:    Puts the frames into the window and calls the methods to build the widgets
        """     
        HEADER_HEIGHT = 72
    
        master.title("IMS Regression Test")
        #master.resizable(False,False)
        photo = tk.PhotoImage(file=os.path.dirname(__file__)+"\\ons.gif")
        master.tk.call('wm','iconphoto',master._w,photo)

        t_frame = tk.Frame(master, height=HEADER_HEIGHT)
        m1_frame = tk.Frame(master)
        m2_frame = tk.Frame(master)
        b_frame = tk.Frame(master)
  
        m1_frame.columnconfigure(0, weight=0)
        m1_frame.columnconfigure(1, weight=1)

        m2_frame.columnconfigure(0, weight =1)
        m2_frame.rowconfigure(0, weight =1)
        
        m2_frame.columnconfigure(0, weight =1)
        
        t_frame.grid(row =0, column=0, columnspan=2, sticky ="nwe")
        m1_frame.grid(row=1, column=0, padx = 25, pady = 5, sticky = "wesn")
        m2_frame.grid(row=1, column =1,padx = 25, pady = 5, sticky = "wesn")
        b_frame.grid(row=2, column =0,padx = 25, columnspan =2, pady = 20, sticky = "wes")

        self.build_ons_banner(t_frame)
        self.build_middle(m1_frame)
        self.build_checkboxes(m1_frame)
        self.build_bottom(b_frame)
        self.build_log_window(m2_frame)

    def build_ons_banner(self,master):
        """
        Author:     Jacob West
        Date:       25/01/2018
        Purpose:    Builds the ONS banner and places it in the top frame 
        """
        image = Image.open("banner2.jpg")
        self.logo = ImageTk.PhotoImage(image)
        self.logo_img = tk.Label(master, image=self.logo, bd=0).place(x=0, y=0)
        
    def build_middle(self, master):
        
        url_lab = tk.Label(master, text = "URL:",  anchor="e", width =9)
        user_lab = tk.Label(master, text = "Username:",  anchor="e", width =9)
        pass_lab = tk.Label(master, text = "Password:", anchor="e", width =9)
        offset_lab = tk.Label(master, text = "Offset:", anchor="e", width =9)
        
        master.update()
        
        self.url_Etry = tk.Entry(master)
        self.user_Etry = tk.Entry(master)
        self.pass_Etry = tk.Entry(master, show ="*")
        self.offset_Etry = tk.Entry(master, width = 5)
        
        url_lab.grid(row=0,column=0, pady=3, sticky ="w")
        self.url_Etry.grid(row=0,column=1, pady=3, sticky ="we")
        
        user_lab.grid(row=1,column=0, pady=3, sticky ="w")
        self.user_Etry.grid(row=1,column=1, pady=3, sticky ="we")
        
        pass_lab.grid(row=2,column=0, sticky ="w")
        self.pass_Etry.grid(row=2,column=1, pady=3, sticky ="we")
        
        offset_lab.grid(row=3,column=0, sticky ="w")
        self.offset_Etry.grid(row=3,column=1, sticky="w")
        
    def load_ims_input_data_command(self, master):

        if self.option1_bool:
            self.new_frame.destroy()
            
            self.IPS_provisional_var.set(0)
            self.asylum_seekers_provisional_var.set(0)
            self.asylum_seekers_nass_var.set(0)
            self.immigration_country_last_residence_var.set(0)
            self.immigration_emigration_by_age_sex_provisional_var.set(0)
            self.immigration_reason_migration_provisional_var.set(0)
            
            self.option1_bool = False
        else:
            self.build_load_ims_input_data_sub_options(master)
            self.option1_bool = True
            
    def perform_ltim_processing_command(self, master):
    
        if self.option2_bool:
            self.new2_frame.destroy()
            
            self.migrant_switchers_var.set(0)
            self.visitor_switchers_var.set(0)
            self.northern_ireland_run_var.set(0)
            self.process_as_data_var.set(0)
            self.apply_LTIM_run_var.set(0)
     
            self.option2_bool = False
        else:
            self.build_perform_ltim_processing_sub_options(master)       
            
            self.option2_bool = True
            
    def export_command(self, master):
   
        if self.option3_bool:
            self.new3_frame.destroy()
            
            self.export_asylum_seekers_by_age_and_sex_var.set(0)
            self.export_asylum_seekers_by_gor.set(0)
            
            self.option3_bool = False

        else:
            self.build_export_sub_options(master)
            self.option3_bool = True
            
        
    def process_historics_command(self, master):
  
        if self.option4_bool:
            self.new4_frame.destroy()
            
            self.q1_var.set(0)
            self.q2_var.set(0)
            self.q3_var.set(0)
            self.q4_var.set(0)
          
            self.option4_bool = False
        else:
            self.build_process_historics_sub_options(master)
            self.option4_bool = True
        
    def build_button(self, master):
    
        text = "Go"
        self.buttonState = "disabled"      
        self.go_btn = tk.Button(self.b_frame, width=10, 
                                text=text, 
                                #state=self.buttonState, 
                                command=lambda : self.go_command(master),
                                cursor="hand2",
                                underline=0)
        
        self.go_btn.grid(row=0, column=0)
    
    def build_option_menu(self):
        options =[1,2,3]
        var = tk.StringVar(self.window)
        var.set(options[0])
        op_menu = tk.OptionMenu(self.m_frame, var, *options)
        op_menu.grid(row=4,column=1, sticky="w", pady = 3) 
        
    def build_checkboxes(self, master):
        
        options_frame = tk.Frame(master)

        log_in_frame = tk.Frame(options_frame)
        load_ims_input_data_frame = tk.Frame(options_frame)
        perform_ips_processing_frame = tk.Frame(options_frame)
        perform_ltim_processing_frame = tk.Frame(options_frame)
        export_frame = tk.Frame(options_frame)
        process_historics_frame = tk.Frame(options_frame)
        process_final_run_frame = tk.Frame(options_frame)
        
        self.option1_bool=True
        self.option2_bool=True
        self.option3_bool=True
        self.option4_bool=True

        self.log_in_var = tk.IntVar(value=1)
        self.load_ims_input_data_var = tk.IntVar(value=1)
        self.perform_ips_processing_var = tk.IntVar(value=1)
        self.perform_ltim_processing_var = tk.IntVar(value=1)
        self.export_var = tk.IntVar(value=1)
        self.process_historics_var = tk.IntVar(value=1)
        self.process_final_run_var = tk.IntVar(value=1)
          
        tk.Checkbutton(log_in_frame, text="Log In", variable=self.log_in_var, cursor="hand2").grid(sticky ="w")
        tk.Checkbutton(load_ims_input_data_frame, text="Load IMS Input Data", variable=self.load_ims_input_data_var, cursor="hand2", command = lambda : self.load_ims_input_data_command(load_ims_input_data_frame)).grid(sticky ="w")           
        tk.Checkbutton(perform_ips_processing_frame, text="Perform IMS Pocessing", variable=self.perform_ips_processing_var, cursor="hand2").grid(sticky ="w")
        tk.Checkbutton(perform_ltim_processing_frame, text="Perform LTIM Processing", variable=self.perform_ltim_processing_var, cursor="hand2", command = lambda : self.perform_ltim_processing_command(perform_ltim_processing_frame)).grid(sticky ="w")
        tk.Checkbutton(export_frame, text="Export", variable=self.export_var, cursor="hand2", command = lambda : self.export_command(export_frame)).grid(sticky ="w")
        tk.Checkbutton(process_historics_frame, text="Process Historics", variable=self.process_historics_var, cursor="hand2", command = lambda : self.process_historics_command(process_historics_frame)).grid(sticky ="w")
        tk.Checkbutton(process_final_run_frame, text="process_final_run", variable=self.process_final_run_var, cursor="hand2").grid(sticky ="w")

        options_frame.columnconfigure(0, weight=1)
        
        log_in_frame.columnconfigure(0, weight=1)
        load_ims_input_data_frame.columnconfigure(0, weight=1)
        perform_ips_processing_frame.columnconfigure(0, weight=1)
        perform_ltim_processing_frame.columnconfigure(0, weight=1)
        export_frame.columnconfigure(0, weight=1)
        process_historics_frame.columnconfigure(0, weight=1)
        process_final_run_frame.columnconfigure(0, weight=1)

        options_frame.grid(row =4, column =0, columnspan =2, pady=15, sticky="we")
        
        log_in_frame.grid(row =0, column =0, pady = 3, sticky="we")
        load_ims_input_data_frame.grid(row =1, column =0, pady = 3, sticky="we")
        perform_ips_processing_frame.grid(row =2, column =0, pady = 3, sticky="we")
        perform_ltim_processing_frame.grid(row =3, column =0, pady = 3, sticky="we")
        export_frame.grid(row =4, column =0, pady = 3, sticky="we")
        process_historics_frame.grid(row =5, column =0, pady = 3, sticky="we")
        process_final_run_frame.grid(row =6, column =0, pady = 3, sticky="we")
         
        self.build_load_ims_input_data_sub_options(load_ims_input_data_frame)      
        self.build_perform_ltim_processing_sub_options(perform_ltim_processing_frame)   
        self.build_export_sub_options(export_frame)
        self.build_process_historics_sub_options(process_historics_frame)
        
        
    def build_log_window(self, master):
        master.update()
        scrollbarv = tk.Scrollbar(master)
        scrollbarv.grid(row = 0, column=1, sticky="ns")
        
        scrollbarh = tk.Scrollbar(master, orient="horizontal")
        scrollbarh.grid(row=1,column=0, sticky = "we")
        
        self.log_lab = tk.Text(master, width =20, height =10, wrap="none",  yscrollcommand=scrollbarv.set, xscrollcommand=scrollbarh.set )
        scrollbarv.config(command=self.log_lab.yview)
        scrollbarh.config(command=self.log_lab.xview)
        
        self.log_lab.grid(row=0, column=0, sticky="news")
 
    def log(self,log):
        
        self.log_lab.insert("end", log + "\n")
        self.log_lab.update()
        
    def button_command(self, master):
     
        self.stop_button.destroy()
        
        helv36 = font.Font(family='Helvetica', size=50, weight=font.BOLD)
        self.stop_button = tk.Button(master, text = "Stop", background = "red", cursor="hand2",
                                     bd = 3, relief ="raised", command = lambda: self.stop_button_command(), 
                                     font = helv36).pack(fill="both", expand = "true")
        
        self.window.state('zoomed')
        messagebox.showinfo("Important Info", "Insure that Internet explorer is open, full screen and zoomed at 75%. \nThank You")
    
    def stop_button_command(self):
        pass
        
    
    def build_bottom(self, master):
        
        helv36 = font.Font(family='Helvetica', size=10)
        self.stop_button = tk.Button(master, text ="GO", width=20, command = lambda: self.button_command(master), 
                                     cursor="hand2",bd = 3, relief ="raised", font = helv36)
        
        self.stop_button.pack(fill="both", expand="true")
        
    def build_load_ims_input_data_sub_options(self, master):
        self.new_frame = tk.LabelFrame(master)
        self.new_frame.columnconfigure(0, weight=1)
        self.new_frame.columnconfigure(1, weight=1)

        self.IPS_provisional_var = tk.IntVar(value=1)
        self.asylum_seekers_provisional_var = tk.IntVar(value=1)
        self.asylum_seekers_nass_var = tk.IntVar(value=1)
        self.immigration_country_last_residence_var = tk.IntVar(value=1)
        self.immigration_emigration_by_age_sex_provisional_var = tk.IntVar(value=1)
        self.immigration_reason_migration_provisional_var = tk.IntVar(value=1)
        
        tk.Checkbutton(self.new_frame, text="IPS provisional", 
                       variable=self.IPS_provisional_var, cursor="hand2").grid(
                                                                        row = 0, column=0, sticky = "w", pady = 3)
        
        tk.Checkbutton(self.new_frame, text="Asylum Seekers Provisional", 
                       variable=self.asylum_seekers_provisional_var, cursor="hand2").grid(
                                                                        row = 0, column=1, sticky = "w", pady = 3)
        
        tk.Checkbutton(self.new_frame, text="Asylum Seekers Nassl",
                       variable=self.asylum_seekers_nass_var, cursor="hand2").grid(
                                                                        row = 0, column=2, sticky = "w", pady = 3)
        
        tk.Checkbutton(self.new_frame, text="NISRA Immigration by Country of Last Residence Provisional", 
                       variable=self.immigration_country_last_residence_var, cursor="hand2").grid(
                                                                        row = 1, column=0,columnspan = 2, sticky = "w", pady = 3)
        
        tk.Checkbutton(self.new_frame, text="NISRA Immigration and Emigration by Age and Sex Provisional", 
                       variable=self.immigration_emigration_by_age_sex_provisional_var, cursor="hand2").grid(
                                                                        row = 2, column=0,columnspan = 2, sticky = "w", pady = 3)
        
        tk.Checkbutton(self.new_frame, text="NISRA Immigration by Reason for Migration Provisional", 
                       variable=self.immigration_reason_migration_provisional_var, cursor="hand2").grid(
                                                                        row = 3, column=0,columnspan = 2, sticky = "w", pady = 3)

        self.new_frame.grid(row=1, column =0, sticky = "wens", padx=10)
        
    def build_perform_ltim_processing_sub_options(self, master):
        self.new2_frame = tk.LabelFrame(master)
            
        self.new2_frame.columnconfigure(0, weight=1)
        self.new2_frame.columnconfigure(1, weight=1)
 
            
        self.migrant_switchers_var = tk.IntVar(value=1)
        self.visitor_switchers_var = tk.IntVar(value=1)
        self.northern_ireland_run_var = tk.IntVar(value=1)
        self.process_as_data_var = tk.IntVar(value=1)
        self.apply_LTIM_run_var = tk.IntVar(value=1)
                    
        tk.Checkbutton(self.new2_frame, text="IMS Migrant Switchers", 
                       variable=self.migrant_switchers_var, cursor="hand2").grid(
                                                                    row = 0, column=0, sticky = "w", pady = 3)
        
        tk.Checkbutton(self.new2_frame, text="IMS Visitor Switchers", 
                       variable=self.visitor_switchers_var, cursor="hand2").grid(
                                                                    row = 0, column=1,sticky = "w", pady = 3)
        
        tk.Checkbutton(self.new2_frame, text="IMS Northern Ireland Run", 
                       variable=self.northern_ireland_run_var, cursor="hand2").grid(
                                                                    row = 0, column=2, sticky = "w", pady = 3)
        
        tk.Checkbutton(self.new2_frame, text="IMS Process AS Data", 
                       variable=self.process_as_data_var, cursor="hand2").grid(
                                                                    row = 1, column=0, sticky = "w", pady = 3)
        
        tk.Checkbutton(self.new2_frame, text="Apply LTIM Run", 
                       variable=self.apply_LTIM_run_var, cursor="hand2").grid(
                                                                    row = 1, column=1, sticky = "w", pady = 3)
        
        self.new2_frame.grid(row = 1, column =0, sticky ="we", padx=10)
        
    def build_export_sub_options(self, master):
        
        self.new3_frame = tk.LabelFrame(master)
            
            
        self.export_asylum_seekers_by_age_and_sex_var = tk.IntVar(value=1)
        self.export_asylum_seekers_by_gor = tk.IntVar(value=1)
                    
        tk.Checkbutton(self.new3_frame, text="Export Asylum Seekers by age and sex", 
                       variable=self.export_asylum_seekers_by_age_and_sex_var, cursor="hand2").grid(
                                                                    row = 0, column=0,sticky = "w", pady = 3)

        tk.Checkbutton(self.new3_frame, text="Export Asylum Seekers by gor", 
                       variable=self.export_asylum_seekers_by_gor, cursor="hand2").grid(
                                                                    row = 1, column=0, sticky = "w", pady = 3)

        self.new3_frame.grid(row = 2, column =0, sticky ="we", padx=10)
        
    def build_process_historics_sub_options(self, master):
        self.new4_frame = tk.LabelFrame(master)
        
        for x in range(0,4):
            self.new4_frame.columnconfigure(x, weight=1)
        
        self.q1_var = tk.IntVar(value=1)
        self.q2_var = tk.IntVar(value=1)
        self.q3_var = tk.IntVar(value=1)
        self.q4_var = tk.IntVar(value=1)
                
        tk.Checkbutton(self.new4_frame, text="Q1", variable=self.q1_var, cursor="hand2").grid(row = 0, column=0,
                                                                                    sticky = "w", pady = 3)
        
        tk.Checkbutton(self.new4_frame, text="Q2", variable=self.q2_var, cursor="hand2").grid(row = 0, column=1,
                                                                                    sticky = "w", pady = 3)
        
        tk.Checkbutton(self.new4_frame, text="Q3", variable=self.q3_var, cursor="hand2").grid(row = 0, column=2,
                                                                                    sticky = "w", pady = 3)
        
        tk.Checkbutton(self.new4_frame, text="Q4", variable=self.q4_var, cursor="hand2").grid(row = 0, column=3,
                                                                                    sticky = "w", pady = 3)
        
        self.new4_frame.grid(row = 2, column =0, sticky ="we", padx=10)
        
        
    