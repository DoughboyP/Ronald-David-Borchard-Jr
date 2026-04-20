"""
Ronald David Borchard Jr - Adventure Game
Main entry point - Select and play any chapter
"""

import sys

def main():
    print("=" * 60)
    print("RONALD DAVID BORCHARD JR - LIFE ADVENTURE GAME")
    print("=" * 60)
    print("\nWelcome! Select a chapter to experience:")
    print("\n1. Birth to Infancy (Ages 0-5)")
    print("2. Childhood (Ages 5-12)")
    print("3. Adolescence (Ages 12-18)")
    print("4. Young Adulthood (Ages 18-25)")
    print("5. Adulthood to Present (Ages 25+)")
    print("6. View Full Story")
    print("0. Exit")
    
    choice = input("\nEnter chapter number (0-6): ")
    
    if choice == "1":
        print("\n📖 Loading Chapter 1: Birth to Infancy...\n")
        from chapters.chapter_1_infancy import InfancyGame
        game = InfancyGame()
        game.start_game()
    elif choice == "2":
        print("\n📖 Loading Chapter 2: Childhood...\n")
        from chapters.chapter_2_childhood import ChildhoodGame
        game = ChildhoodGame()
        game.start_game()
    elif choice == "3":
        print("\n📖 Loading Chapter 3: Adolescence...\n")
        from chapters.chapter_3_adolescence import AdolescenceGame
        game = AdolescenceGame()
        game.start_game()
    elif choice == "4":
        print("\n📖 Loading Chapter 4: Young Adulthood...\n")
        from chapters.chapter_4_young_adulthood import YoungAdulthoodGame
        game = YoungAdulthoodGame()
        game.start_game()
    elif choice == "5":
        print("\n📖 Loading Chapter 5: Adulthood to Present...\n")
        from chapters.chapter_5_adulthood_present import AdulthoodPresentGame
        game = AdulthoodPresentGame()
        game.start_game()
    elif choice == "6":
        print("\n📖 Full Story Overview\n")
        print_full_story()
    elif choice == "0":
        print("\n👋 Thanks for playing!\n")
        sys.exit()
    else:
        print("\n❌ Invalid choice. Please try again.\n")
        main()

def print_full_story():
    print("=" * 60)
    print("THE COMPLETE STORY OF RONALD DAVID BORCHARD JR")
    print("=" * 60)
    print("""\nFrom Birth to Present Day (2026)\n\nRonald David Borchard Jr was born into a world of infinite possibilities.
His journey began as a helpless infant and evolved through distinct life chapters:\n\n🍼 INFANCY (0-5): Discovering the world, first bonds, first steps, first words\n👦 CHILDHOOD (5-12): School, friendships, interests, personality formation\n👨 ADOLESCENCE (12-18): Identity, romance, major decisions, growth\n👨‍💼 YOUNG ADULTHOOD (18-25): Independence, career, relationships, adult responsibilities\n👨‍💼 ADULTHOOD TO PRESENT (25+): Leadership, legacy, family, impact\n\nEach chapter contains meaningful choices that shape the narrative.
Play through each chapter to experience Ronald's complete life story!\n    """)
    print("=" * 60)
    input("\nPress ENTER to return to menu...")
    main()

if __name__ == "__main__":
    main()