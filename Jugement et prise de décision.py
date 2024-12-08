import streamlit as st
import random
import pandas as pd
from datetime import datetime

class ExperienceInvestissement:
    def __init__(self):
        # Initialisation des variables de session
        if 'resultats' not in st.session_state:
            st.session_state.resultats = []
        if 'tour_actuel' not in st.session_state:
            st.session_state.tour_actuel = 1
        if 'dotation_initiale' not in st.session_state:
            st.session_state.dotation_initiale = 100

    def generer_resultat_de(self, probabilite_gain=0.5):
        """
        Génération objective du résultat du dé
        
        Args:
            probabilite_gain (float): Probabilité de gagner (défaut 50%)
        
        Returns:
            str: 'Gain' ou 'Perte'
        """
        return 'Gain' if random.random() < probabilite_gain else 'Perte'

    def calculer_gain(self, resultat, decision, montant_initial=10):
        """
        Calcule le gain/perte en fonction du résultat et de la décision
        
        Args:
            resultat (str): 'Gain' ou 'Perte'
            decision (str): 'Conserver' ou 'Vendre'
            montant_initial (int): Montant du pari à chaque tour
        
        Returns:
            float: Montant gagné ou perdu
        """
        if resultat == 'Gain' and decision == 'Conserver':
            return montant_initial
        elif resultat == 'Perte' and decision == 'Vendre':
            return 0
        elif resultat == 'Perte' and decision == 'Conserver':
            return -montant_initial
        return 0

    def interface_principale(self):
        """
        Interface principale de l'expérience
        """
        st.title("🎲 Expérience de Décision d'Investissement")
        
        # Section de consentement
        if not st.session_state.get('consentement', False):
            self.page_consentement()
            return

        # Informations personnelles
        if not st.session_state.get('info_personnelles', False):
            self.page_informations_personnelles()
            return

        # Sélection de la condition
        if not st.session_state.get('condition_selectionnee', False):
            self.page_selection_condition()
            return

        # Simulation des tours
        self.page_simulation_tours()

    def page_consentement(self):
        """
        Page de consentement éthique
        """
        st.header("Consentement Éthique")
        
        consentement = st.checkbox("J'ai lu et je comprends les conditions de l'étude")
        
        if consentement:
            st.session_state.consentement = True
            st.experimental_rerun()

    def page_informations_personnelles(self):
        """
        Collecte des informations personnelles
        """
        st.header("Informations Personnelles")
        
        age = st.slider("Âge", 18, 99, 25)
        genre = st.selectbox("Genre", ["Homme", "Femme", "Autre", "Préfère ne pas répondre"])
        
        if st.button("Continuer"):
            st.session_state.age = age
            st.session_state.genre = genre
            st.session_state.info_personnelles = True
            st.experimental_rerun()

    def page_selection_condition(self):
        """
        Sélection de la condition expérimentale
        """
        st.header("Condition Expérimentale")
        
        condition = st.radio("Choisissez votre condition", 
                             ['Décision Séquentielle', 'Décision Planifiée'])
        
        if st.button("Confirmer"):
            st.session_state.condition = condition
            st.session_state.condition_selectionnee = True
            st.experimental_rerun()

    def page_simulation_tours(self):
        """
        Simulation des tours de l'expérience
        """
        st.header(f"Tour {st.session_state.tour_actuel}")
        
        # Génération du résultat
        resultat = self.generer_resultat_de()
        st.write(f"📊 Résultat du dé : {resultat}")
        
        # Affichage de la dotation
        st.write(f"Votre dotation actuelle : {st.session_state.dotation_initiale} ECU")
        
        # Choix de décision
        decision = st.radio("Votre décision", ['Conserver', 'Vendre'])
        
        if st.button("Confirmer ma décision"):
            # Calcul du gain/perte
            gain = self.calculer_gain(resultat, decision)
            st.session_state.dotation_initiale += gain
            
            # Stockage du résultat
            resultat_tour = {
                'Tour': st.session_state.tour_actuel,
                'Résultat': resultat,
                'Décision': decision,
                'Gain/Perte': gain
            }
            st.session_state.resultats.append(resultat_tour)
            
            # Passage au tour suivant
            st.session_state.tour_actuel += 1
            
            # Vérification de fin d'expérience
            if st.session_state.tour_actuel > 5:
                self.page_resultats_finaux()
            else:
                st.experimental_rerun()

    def page_resultats_finaux(self):
        """
        Affichage et export des résultats finaux
        """
        st.header("Résultats Finaux")
        
        # Création du DataFrame
        df_resultats = pd.DataFrame(st.session_state.resultats)
        st.table(df_resultats)
        
        # Résumé
        st.write(f"Dotation finale : {st.session_state.dotation_initiale} ECU")
        st.write(f"Condition : {st.session_state.condition}")
        
        # Export des données
        if st.download_button(
            label="Télécharger les résultats",
            data=df_resultats.to_csv(index=False),
            file_name=f'resultats_experience_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv'
        ):
            st.success("Résultats exportés avec succès !")

def main():
    """
    Fonction principale de l'application Streamlit
    """
    experience = ExperienceInvestissement()
    experience.interface_principale()

if __name__ == "__main__":
    main()








