#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

def simulation_neutrino_complete():
    # ==========================================
    # 1. PARAMÈTRES PHYSIQUES
    # ==========================================
    L = 10000              # Distance (km)
    dm2 = 2.5e-3           # Delta m^2 (eV^2)
    theta_deg = 45.0       # Angle de mélange (degrés)
    z = 0.1                # Redshift
    alpha = 2.0            # Indice spectral de la source
    
    # Grille d'énergie (GeV)
    E_source = np.logspace(0, 2, 1000) 
    E_terre = E_source / (1 + z)

    # ==========================================
    # 2. CALCUL DES FLUX ET OSCILLATIONS
    # ==========================================
    # Flux initial (Source 100% muonique)
    flux_total = E_source**(-alpha)
    flux_mu_prop = (flux_total / (1 + z))
    
    # Formule PMNS
    theta_rad = np.radians(theta_deg)
    sin2_2theta = np.sin(2 * theta_rad)**2
    arg = 1.27 * dm2 * L / E_terre
    prob_conversion = sin2_2theta * np.sin(arg)**2
    prob_survie = 1.0 - prob_conversion

    # Flux finaux sur Terre
    flux_mu_terre = flux_mu_prop * prob_survie
    flux_e_terre = flux_mu_prop * prob_conversion

    # ==========================================
    # 3. CRÉATION DES 4 TRACÉS
    # ==========================================
    fig, axs = plt.subplots(2, 2, figsize=(15, 12))
    plt.subplots_adjust(hspace=0.3, wspace=0.25)

    # --- TRACÉ 1 : Spectres des Flux ---
    axs[0, 0].plot(E_terre, flux_mu_prop, 'k--', alpha=0.3, label='Sans oscillation')
    axs[0, 0].plot(E_terre, flux_mu_prop, color='blue', label=r'Flux Muon ($\nu_\mu$)')
    axs[0, 0].plot(E_terre, flux_e_terre, color='red', label=r'Flux Électron ($\nu_e$)')
    axs[0, 0].set_xscale('log')
    axs[0, 0].set_yscale('log')
    axs[0, 0].set_title("1. Spectres d'Énergie sur Terre")
    axs[0, 0].set_xlabel("E [GeV]")
    axs[0, 0].set_ylabel("dN/dE")
    axs[0, 0].legend()

    # --- TRACÉ 2 : Ratio d'Atténuation (Data/MC simple) ---
    # Utile pour comparer avec KM3NeT ou IceCube
    ratio_transition = flux_e_terre / flux_mu_prop
    axs[0, 1].plot(E_terre, ratio_transition, color='purple', lw=2)
    axs[0, 1].axhline(0.5, color='black', ls=':', label='Mélange Max (0.5)')
    axs[0, 1].set_xscale('log')
    axs[0, 1].set_ylim(0, 1.1)
    axs[0, 1].set_title("2. Ratio de Transition : Electron / Muon ")
    axs[0, 1].set_xlabel("E [GeV]")
    axs[0, 1].set_ylabel(r"Prpbabilité de Transition$P_{\mu e}$")
    axs[0, 1].legend()

    # --- TRACÉ 3 : Probabilité en fonction de L/E ---
    # Le tracé de validation physique classique
    le_ratio = L / E_terre
    axs[1, 0].plot(le_ratio, prob_conversion, color='red')
    axs[1, 0].set_title(r"3. Validation Physique : $P_{\mu e}$ vs $L/E$")
    axs[1, 0].set_xlabel(r"$L/E$ [km/GeV]")
    axs[1, 0].set_ylabel("Probabilité de Transition")
    axs[1, 0].grid(alpha=0.3)

    # --- TRACÉ 4 : Oscillogramme (Distance vs Énergie) ---
    # On crée une grille 2D pour voir l'effet de la distance
    distances = np.linspace(0, 15000, 200)
    energies = np.logspace(0, 2, 200)
    E_grid, L_grid = np.meshgrid(energies, distances)
    # Calcul de la probabilité sur toute la grille    
    prob_grid = sin2_2theta * np.sin(1.27 * dm2 * L_grid / E_grid)**2
    
    im = axs[1, 1].pcolormesh(E_grid, L_grid, prob_grid, cmap='RdYlBu', shading='auto')
    axs[1, 1].set_xscale('log')
    axs[1, 1].set_title(r"4. Oscillogramme de Transition ($P_{\mu e}$)")
    axs[1, 1].set_xlabel("E [GeV]")
    axs[1, 1].set_ylabel("Distance L [km]")
    fig.colorbar(im, ax=axs[1, 1], label="Probabilité de Transition ")

  # Finalisation
    plt.suptitle(f"Analyse des Oscillations de Neutrinos (PMNS 2 saveurs)\n"
                 f"$\Delta m^2 = {dm2}$ eV², $\\theta = {theta_deg}^\circ$", fontsize=16)
    
    plt.savefig('analyse_complete_neutrinos.png', dpi=300)
    print("✅ Analyse complète terminée. Image : 'analyse_complete_neutrinos.png'")
    #plt.show()

if __name__ == "__main__":
    simulation_neutrino_complete() 
