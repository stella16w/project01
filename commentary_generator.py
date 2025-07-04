import random
from gtts import gTTS
import pygame
import tempfile
import os

class CommentaryGenerator:
    def __init__(self):
        self.templates = {
            'shot': [
                "What a shot! The ball is flying towards the goal!",
                "A powerful strike! The keeper needs to be alert!",
                "Shot on target! This could be dangerous!",
                "The player unleashes a fierce shot!"
            ],
            'pass': [
                "Nice pass! The ball is moving across the field!",
                "A good pass to a teammate!",
                "The ball is being distributed well!",
                "Excellent ball movement!"
            ],
            'player_interaction': [
                "Player gets on the ball!",
                "Someone's taking control of the ball!",
                "A player is making a move!",
                "The ball is being contested!"
            ],
            'goal_area_activity': [
                "Danger in the goal area!",
                "The ball is in a dangerous position!",
                "Action near the goal!",
                "This could be a scoring opportunity!"
            ],
            'general': [
                "Great football action!",
                "The game is heating up!",
                "Excellent play from both teams!",
                "What an exciting moment!"
            ]
        }
        
        pygame.mixer.init()
    
    def generate_commentary_text(self, events):
        """Generate commentary text based on events"""
        if not events:
            return random.choice(self.templates['general'])
        
        # Find the most significant event
        priority_order = ['goal_area_activity', 'shot', 'pass', 'player_interaction']
        
        selected_event = None
        for event_type in priority_order:
            for event in events:
                if event['type'] == event_type:
                    selected_event = event
                    break
            if selected_event:
                break
        
        if not selected_event:
            selected_event = events[0]
        
        # Generate commentary based on event type
        event_type = selected_event['type']
        if event_type in self.templates:
            commentary = random.choice(self.templates[event_type])
        else:
            commentary = random.choice(self.templates['general'])
        
        # Add context if multiple events
        if len(events) > 1:
            commentary += " There's a lot of action happening on the field!"
        
        return commentary
    
    def text_to_speech(self, text, language='en'):
        """Convert text to speech and play it"""
        try:
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
                tts.save(tmp_file.name)
                
                # Play the audio
                pygame.mixer.music.load(tmp_file.name)
                pygame.mixer.music.play()
                
                # Wait for playback to finish
                while pygame.mixer.music.get_busy():
                    pygame.time.wait(100)
                
                # Clean up
                pygame.mixer.music.unload()
                os.unlink(tmp_file.name)
                
        except Exception as e:
            print(f"Error generating speech: {e}")
    
    def generate_commentary(self, events):
        """Generate and play commentary for events"""
        commentary_text = self.generate_commentary_text(events)
        print(f"Commentary: {commentary_text}")
        self.text_to_speech(commentary_text)
        return commentary_text