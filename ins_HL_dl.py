import subprocess
import os
from typing import Union
import instaloader
import ins_donwloader_db as db
import instaloader_firefox_login as firefox_login

DL = instaloader.Instaloader()

class Highlightsloader:
    
    def __init__(self) -> None:

        """
        Parameters:
        self.admin_username (str): An Instagram account must be logged in on the firefox browser before running this script
        self.target_list (list): A list of instagram account you'd like to download

        """
    
        self.admin_username = firefox_login.username
        self.target_list = ['']
        folder = 'story_and_highlights'
        self.main_download_folder_path = os.path.join(os.getcwd(), folder)

    def create_user_folder(self, target) -> None:
        """
        Summary of the Function:
        Create a downloaded account folder to save the highlights
        
        """
        
        if not os.path.exists(self.main_download_folder_path):
            os.mkdir(self.main_download_folder_path)
        
        self.user_main_path = os.path.join(self.main_download_folder_path, target)
        if not os.path.exists(self.user_main_path):
            os.mkdir(self.user_main_path)

        self.user_main_folder = f'{self.target_username}_highlights_{self.target_userid}'

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

    def download_user_highlights(self):
        """
        Summary of the Function:
        Download the highlights of the targeted account (Default: All Highlights)

        """

        command = [
            "instaloader",
            "--latest-stamps",
            "--login",
            self.admin_username,
            "--no-posts",
            "--highlights",
            "--no-profile-pic",
            "--no-video-thumbnails",
            "--no-metadata-json", 
            "--no-compress-json",
            "--dirname-pattern", f"{self.user_main_path}/{self.user_main_folder}",
            self.target_username,
        ]

        try:
            subprocess.run(command, check=True)
            print("Instaloader command completed successfully.")

        except subprocess.CalledProcessError as e:
            print(f"Error running Instaloader command: {e}")
            exit()

def main():
    highlightsdl = Highlightsloader()
    def download_run():
        """
        Summary of the Function:
        Get the data of targeted instagram account, and then start downloading their highllights

        """

        for target in highlightsdl.target_list:
            profile_dict = highlightsdl.get_user_profile(target)

            if profile_dict != False: # profile is existing on instagram = True
                highlightsdl.create_user_folder(target)

                try:
                    located_path = os.path.join(highlightsdl.user_main_path, highlightsdl.user_main_folder)
                    if not os.path.exists(located_path):
                        highlightsdl.download_user_highlights()

                except instaloader.exceptions.QueryReturnedBadRequestException as e:
                    print(f'''---------------------------------------------------------------------\n
An error occurred: {str(e)}\n
---------------------------------------------------------------------\n''')
                    exit()
                    
    download_run()
    
if __name__=='__main__':
    main()