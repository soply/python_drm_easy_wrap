library(drc)
library(stringr)
library(tools)

#curve fitting iteration function
curveFits <- function(Dose, Response){
  #try log-logistic
  drm_fit <- drm(Response ~ Dose,fct = LL.4(fixed = c(NA, NA, NA, NA), names = c("Slope", "Lower Limit", "Upper Limit", "IC50")), control = drmc(errorm = FALSE))
  drm_fit$fit_type <- "LL4"
  if('convergence' %in% names(drm_fit)){
    #if no convergence, try logistic
    drm_fit <- drm(Response ~ Dose,fct = L.4(fixed = c(NA, NA, NA, NA), names = c("Slope", "Lower Limit", "Upper Limit", "IC50")), control = drmc(errorm = FALSE))
    drm_fit$fit_type <- "L4"
  }
  if('convergence' %in% names(drm_fit)){
    #still no convergence, set fit parameters to NA
    drm_fit$coefficients <- c("","","","")
    drm_fit$fit_type <- "none"
    drm_fit$fit$value <- NA
  }
  return(drm_fit)
}
