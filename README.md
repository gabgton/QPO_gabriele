# QPO_polarization_analysis
This repository contains codes and scripts to study the correlation between the X-ray polarization and the Quasi Periodic Oscillations in Black Hole X-ray Binaries. This strategy combines both power spectra and polarization analyses using the `stingray` and `ixpeobssim` software respectively.

## Step 0: GTI treatment and time serie
IXPE's focal plane hosts three Detector Units (DU), each housing one Gas Pixel Detector (GPD), the gas polarimeter based on the photoelectric effect. These DUs act as three distinct telescopes and for these reason they must be treated separately. In our case, it is necessary to correctly use the Good Time Intervals (GTI) of each DU. GTI list the good time intervals of the observation, i.e. the time intervals during which the detector data are considered valid and can be used for scientific analysis. However, the GTIs of the three IXPE’s DUs do not coincide. So, we choose the most conservative option to merge the events from the three telescopes: we make the logical *and* of the three GTIs, creating new *merged GTIs*, and then we select the events whose detection times lie within the latter. The resulting subset of events, together with the new merged GTIs, are used to build the correct time series with `stingray`.

To do so, we use the code:    `make_GTI_intervals.py`

## Step 1: power spectra analysis
`launch_allDUs_qpo_segments.sh` will launch in sequence:
1. `QPO_allDUs_freq_analysis.py`
2. `QPO_allDUs_polar_analysis.py`
3. `QPO_allDUs_stat_analysis.py`


The main challenge of this analysis lies in the fact that the IXPE Level 2 events are recorded and defined in the time domain, whereas QPOs are characterized and analyzed in the Fourier (frequency) domain. To overcome this aspect, we adopted the following strategy.

First of all, the observation power spectrum is evaluated and fitted using a Lorentzian profile 

```math
    f(\nu) = \frac{1}{\pi}\frac{H\gamma}{(\nu-\nu_{\rm qpo})^2+\gamma^2},
```

that allows to characterize the QPOs by their integrated power $H$ (related to the fractional RMS variability), their centroid frequency $\nu_{\rm qpo}$ and their width $\gamma$, defined as the half width half maximum (HWHM).

The whole observation is divided into time segments of given duration, taking into account also the merged GTI. Then the PS in each time segment is built and fitted: I consider here only the contribution from the main QPO peak and the noise. For the parameters, I use the fit of the entire observation as a reference, initializing the Lorentzian parameters accordingly and keeping the others fixed (after correcting for the segment size and statistics).

This is done by the first half of the code `QPO_allDUs_freq_analysis.py`. The QPO peak is then fitted with a *Lorentzian* profile, whose integral is used as a measure of the QPO strength in that segment:

```math
    f_k(\nu) = \frac{1}{\pi}\frac{H_k\gamma_k}{(\nu-\nu_{{\rm qpo},k})^2+\gamma_k^2}
```

The Lorentzian integral is normalized to the integral measured from the Power Spectrum of the entire observation, providing a normalized QPO intensity for each segment.
A threshold is then applied to the normalized QPO intensity. Rather than using a single value, the threshold is scanned over a predefined range (typically spanning the central 95% of the normalized intensity distribution). For each threshold:
- Selected events are those belonging to time segments where the normalized QPO intensity is above the threshold.
- Non-selected events are those belonging to time segments where the normalized QPO intensity is below the threshold.

This procedure is repeated for different threshold values and it generates multiple pairs of event populations. This is done by the second half of `QPO_allDUs_freq_analysis.py`.

These populations will be subsequently analyzed with the polarization pipeline to search for correlations between X-ray polarization and QPO strength.

## Step 2: polarization analysis
The polarization analysis is performed by `QPO_allDUs_polar_analysis.py` using the `ixpeobssim` software package. Using the boolean masks produced with `QPO_allDUs_freq_analysis.py`, `QPO_allDUs_polar_analysis.py` uses `xpselect` to select the events inside and outside the selected or not selected time segments, building the two populations. `xpbin` with the `PCUBE` algorithm evaluates the polarization for each population. 

`polatization_plots_qpo.py` is used to create the contour plots to visually evaluate the polarization difference between the selected and not selected population.

Finally, a `.csv` table is created with `pandas`: it will be used by `QPO_allDUs_stat_analysis.py` to study the significance of the difference in the polarization between the two populations.

## Step 3: statistical analysis
Considering the Stokes parameter Q (the same applies for U), we perform a Welch’s t-test (unequal variance t-test) to test the null hypothesis that two populations have means compatible within their uncertainties:

```math
  t=\frac{Q_{\rm S}-Q_{\rm NS}}{\sqrt{Q^2_{\rm err_{\rm S}}+Q^2_{\rm err_{\rm NS}}}},\quad \text{with}\quad d.o.f.\approx\frac{\left(Q^2_{\rm err_{\rm S}}+Q^2_{\rm err_{\rm NS}}\right)^2}{\frac{Q^4_{\rm err_{\rm S}}}{N_{\rm S}-1}+\frac{Q^4_{\rm err_{\rm NS}}}{N_{\rm NS}-1}},
```

where the subscripts S and NS indicate the selected and not selected population respectively. This test is typically applied when the two samples exhibit unequal variances and may also differ in sample size, as in our case.

`QPO_allDUs_stat_analysis.py` performs this analysis saving the pvalues for Q and U for each threshold value.


## Step 4: comparisons
At this level, given a time segment size, two populations of events have been created comparing the QPO peak intensity to a varying threshold in a specific range (`QPO_allDUs_freq_analysis.py`). Then, the polarization has been calculated (`QPO_allDUs_polar_analysis.py`) and the statistical analysis has been performed (`QPO_allDUs_stat_analysis.py`). 

`launch_allDUs_qpo_segments.sh` performs this analysis for different time segment sizes and every result is saved each time. `QPO_segments_comparison.py` can be used to look at the summary of all the measurements at different time segment sizes, focusing on the statistical aspects (pvalues).

## P.S.
For the moment, some codes have Stefano's paths and similar stuff, I suggest to create a new branch and change the paths there. Maybe, I will fix this aspect or create some gitignores.
