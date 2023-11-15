import instaloader
from typing import Union
import os
import subprocess

DL = instaloader.Instaloader()

class InsDownloader:

    def __init__(self) -> None:
        """
        Parameters:
        self.admin_username (str): The Instagram login account which should already be saved in the session file
        self.target_list (list): A list of instagram account you'd like to download

        """
        self.admin_username =''
        self.target_list = ['']
        folder = 'profile_downloaded'
        self.main_download_folder_path = os.path.join(os.getcwd(), folder)
        
    def login(self) -> None:
        """
        Summary of the Function:
        Log into instagram account, if target is a private account and which is followed by admin account, then login needed for downloading

        """
        DL.load_session_from_file(self.admin_username)
        print('\n-------------------------Login Successfully-------------------------\n')

    def download_user_profile(self) -> None:
        """
        Summary of the Function:
        Download targeted account profile (Default: All Posts)

        """
        os.chdir(self.user_main_folder_path)
        try:
            DL.download_profile(self.target_username, profile_pic_only=False)

        except instaloader.exceptions.PrivateProfileNotFollowedException as e:
            command = [
            "instaloader",
            "--login",
            self.admin_username,
            "--dirname-pattern", f"{self.main_download_folder_path}/{self.user_main_folder}",
            self.target_username
            ]

            try:
                subprocess.run(command, check=True)
                #print("Instaloader command completed successfully.")

            except subprocess.CalledProcessError as e:
                print(f"Error running Instaloader command: {e}")
                exit()
    
    def create_user_folder(self) -> None:
        """
        Summary of the Function:
        Create a downloaded account folder to save the profile
        
        """
        if not os.path.exists(self.main_download_folder_path):
            os.mkdir(self.main_download_folder_path)

        self.user_main_folder = f'{self.target_username}_{self.target_userid}'
        self.user_main_folder_path = os.path.join(self.main_download_folder_path, self.user_main_folder)

        if not os.path.exists(self.user_main_folder_path):
            os.mkdir(self.user_main_folder_path)

    def get_user_profile(self, target) -> Union[dict, bool, bool]:
        """
        Summary of the Function:
        Get the information of the targeted instagram account

        Parameters:
        target (str): the targeted instagram account

        Returns:
        profile_dict (dict): A dict of the profile information
        False (bool): profile doesn't exist
        False (bool): Error 
        
        """
        try:
            profile_dict = {}
            profile = instaloader.Profile.from_username(DL.context, target)
            profile_dict['profile.target_username'] = self.target_username = profile.username
            profile_dict['profile.userid'] = self.target_userid = profile.userid
            profile_dict['profile.full_name'] = profile.full_name
            profile_dict['profile.followers'] = profile.followers
            profile_dict['profile.followees'] = profile.followees
            profile_dict['profile.biography'] = profile.biography
            profile_dict['profile.profile_pic_url'] = self.target_profile_pic_url = profile.profile_pic_url
            print(profile.profile_pic_url)
            print(f'''-------------------------------------------------------------------
                  
Profile Username: {profile.username}
Profile UserID: {profile.userid}
Profile Full Name: {profile.full_name}
Profile Followers: {profile.followers}
Profile Followings: {profile.followees}

-------------------------------------------------------------------\n''')
            return profile_dict
            
        except instaloader.exceptions.ProfileNotExistsException:
            print(f'Profile "{target}" does not exist.')
            return False

        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return False

def main():
    Ins = InsDownloader()
    def download_run():
        """
        Summary of the Function:
        Get the data of targeted instagram account, and then start downloading the profile
        
        """

        for target in Ins.target_list:
            profile_dict = Ins.get_user_profile(target)

            if profile_dict != False: # profile is existing on instagram = True
                Ins.create_user_folder()
                try:
                    Ins.download_user_profile()

                except instaloader.exceptions.LoginRequiredException as e: 
                    Ins.login()
                    Ins.download_user_profile()
                    
                except instaloader.exceptions.QueryReturnedBadRequestException as e:
                    print(f'''---------------------------------------------------------------------\n
An error occurred: {str(e)}\n
---------------------------------------------------------------------\n''')
                    exit()
                    

    download_run()
    
if __name__=='__main__':
    main()







   

        



