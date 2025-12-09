# Statistical Analysis for Pain Management Program Outcomes
# Comprehensive analysis using paired t-tests, ANOVA, and longitudinal modeling

# Load required libraries
library(tidyverse)
library(lme4)         # Linear mixed-effects models
library(nlme)         # Alternative mixed models
library(psych)        # Psychological statistics
library(ggplot2)      # Visualizations
library(gridExtra)    # Multiple plots
library(effsize)      # Effect size calculations
library(car)          # ANOVA
library(knitr)        # Report generation
library(rmarkdown)    # Report generation

# ============================================================================
# 1. DATA LOADING AND PREPARATION
# ============================================================================

load_patient_data <- function(csv_path) {
  # Load patient outcome data
  data <- read.csv(csv_path, stringsAsFactors = FALSE)
  data$log_date <- as.Date(data$log_date)
  data$user_id <- as.factor(data$user_id)
  return(data)
}

calculate_week_number <- function(data) {
  # Calculate week number from dates
  data <- data %>%
    group_by(user_id) %>%
    mutate(week = as.integer((log_date - min(log_date)) / 7) + 1) %>%
    ungroup()
  return(data)
}

create_summary_data <- function(data) {
  # Create weekly summary data
  summary_data <- data %>%
    group_by(user_id, week) %>%
    summarise(
      pain_level_mean = mean(pain_level, na.rm = TRUE),
      sleep_quality_mean = mean(sleep_quality, na.rm = TRUE),
      fatigue_level_mean = mean(fatigue_level, na.rm = TRUE),
      anxiety_level_mean = mean(anxiety_level, na.rm = TRUE),
      function_level_mean = mean(function_level, na.rm = TRUE),
      n_entries = n(),
      .groups = "drop"
    )
  return(summary_data)
}

# ============================================================================
# 2. DESCRIPTIVE STATISTICS
# ============================================================================

calculate_descriptive_stats <- function(data) {
  # Calculate descriptive statistics for all metrics

  metrics <- c("pain_level", "sleep_quality", "fatigue_level",
               "anxiety_level", "function_level")

  results <- list()

  for (metric in metrics) {
    week1_data <- data %>% filter(week == 1) %>% pull(!!metric)
    week8_data <- data %>% filter(week == 8) %>% pull(!!metric)

    results[[metric]] <- list(
      baseline = list(
        mean = mean(week1_data, na.rm = TRUE),
        sd = sd(week1_data, na.rm = TRUE),
        median = median(week1_data, na.rm = TRUE),
        min = min(week1_data, na.rm = TRUE),
        max = max(week1_data, na.rm = TRUE),
        n = sum(!is.na(week1_data))
      ),
      endpoint = list(
        mean = mean(week8_data, na.rm = TRUE),
        sd = sd(week8_data, na.rm = TRUE),
        median = median(week8_data, na.rm = TRUE),
        min = min(week8_data, na.rm = TRUE),
        max = max(week8_data, na.rm = TRUE),
        n = sum(!is.na(week8_data))
      )
    )
  }

  return(results)
}

# ============================================================================
# 3. PAIRED T-TESTS (PRE-POST COMPARISON)
# ============================================================================

perform_paired_ttests <- function(data) {
  # Perform paired t-tests comparing Week 1 vs Week 8

  metrics <- c("pain_level", "sleep_quality", "fatigue_level",
               "anxiety_level", "function_level")

  results <- list()

  for (metric in metrics) {
    # Get paired data (only participants with both week 1 and week 8 data)
    paired_data <- data %>%
      filter(week %in% c(1, 8)) %>%
      select(user_id, week, !!metric) %>%
      pivot_wider(names_from = week, values_from = !!metric,
                  names_prefix = "week_") %>%
      filter(!is.na(week_1) & !is.na(week_8))

    if (nrow(paired_data) > 2) {
      # Perform paired t-test
      t_test <- t.test(paired_data$week_8, paired_data$week_1, paired = TRUE)

      # Calculate effect size (Cohen's d)
      effect <- cohen.d(paired_data$week_8, paired_data$week_1, paired = TRUE)

      results[[metric]] <- list(
        n_pairs = nrow(paired_data),
        mean_baseline = mean(paired_data$week_1),
        mean_endpoint = mean(paired_data$week_8),
        mean_change = mean(paired_data$week_8 - paired_data$week_1),
        t_statistic = t_test$statistic,
        df = t_test$parameter,
        p_value = t_test$p.value,
        ci_lower = t_test$conf.int[1],
        ci_upper = t_test$conf.int[2],
        cohens_d = effect$estimate,
        effect_size_interpretation = interpret_cohens_d(effect$estimate)
      )
    }
  }

  return(results)
}

interpret_cohens_d <- function(d) {
  # Interpret Cohen's d effect size
  abs_d <- abs(d)
  if (abs_d < 0.2) return("negligible")
  if (abs_d < 0.5) return("small")
  if (abs_d < 0.8) return("medium")
  return("large")
}

# ============================================================================
# 4. REPEATED MEASURES ANOVA
# ============================================================================

perform_repeated_measures_anova <- function(data) {
  # Perform repeated measures ANOVA across all 8 weeks

  metrics <- c("pain_level", "sleep_quality", "fatigue_level",
               "anxiety_level", "function_level")

  results <- list()

  for (metric in metrics) {
    # Prepare data for ANOVA
    anova_data <- data %>%
      filter(!is.na(!!sym(metric))) %>%
      mutate(week = as.factor(week))

    # Perform repeated measures ANOVA using lme4
    model <- lmer(as.formula(paste(metric, "~ week + (1|user_id)")),
                  data = anova_data)

    # Get ANOVA table
    anova_result <- anova(model)

    results[[metric]] <- list(
      F_statistic = anova_result$`F value`[1],
      df_num = anova_result$NumDF[1],
      df_den = anova_result$DenDF[1],
      p_value = anova_result$`Pr(>F)`[1],
      significant = anova_result$`Pr(>F)`[1] < 0.05
    )
  }

  return(results)
}

# ============================================================================
# 5. LONGITUDINAL MIXED EFFECTS MODELS
# ============================================================================

fit_longitudinal_models <- function(data) {
  # Fit linear mixed effects models to assess trends over time

  metrics <- c("pain_level", "sleep_quality", "fatigue_level",
               "anxiety_level", "function_level")

  models <- list()
  summaries <- list()

  for (metric in metrics) {
    # Fit linear mixed model with week as continuous predictor
    model <- lmer(as.formula(paste(metric, "~ week + (week|user_id)")),
                  data = data %>% filter(!is.na(!!sym(metric))))

    models[[metric]] <- model

    # Extract key parameters
    fixed_effects <- fixef(model)

    summaries[[metric]] <- list(
      intercept = fixed_effects[1],
      slope = fixed_effects[2],  # Change per week
      slope_se = sqrt(diag(vcov(model)))[2],
      total_change_8_weeks = fixed_effects[2] * 7,  # Weeks 1-8
      slope_p_value = summary(model)$coefficients[2, "Pr(>|t|)"]
    )
  }

  return(list(models = models, summaries = summaries))
}

# ============================================================================
# 6. CLINICAL SIGNIFICANCE ANALYSIS
# ============================================================================

calculate_clinical_significance <- function(data) {
  # Calculate percentage of participants achieving clinically significant improvement

  thresholds <- list(
    pain_level = -2,        # 2+ point reduction
    sleep_quality = 1,      # 1+ point improvement
    fatigue_level = -1,     # 1+ point reduction
    anxiety_level = -2,     # 2+ point reduction
    function_level = 1      # 1+ point improvement
  )

  results <- list()

  for (metric in names(thresholds)) {
    # Get paired data
    paired_data <- data %>%
      filter(week %in% c(1, 8)) %>%
      select(user_id, week, !!metric) %>%
      pivot_wider(names_from = week, values_from = !!metric,
                  names_prefix = "week_") %>%
      filter(!is.na(week_1) & !is.na(week_8)) %>%
      mutate(change = week_8 - week_1)

    # Calculate clinical significance
    threshold <- thresholds[[metric]]

    if (threshold < 0) {
      # For pain/fatigue/anxiety, improvement is reduction
      clinically_improved <- sum(paired_data$change <= threshold)
    } else {
      # For sleep/function, improvement is increase
      clinically_improved <- sum(paired_data$change >= threshold)
    }

    results[[metric]] <- list(
      n_total = nrow(paired_data),
      n_clinically_improved = clinically_improved,
      percentage_improved = (clinically_improved / nrow(paired_data)) * 100,
      threshold = threshold
    )
  }

  return(results)
}

# ============================================================================
# 7. VISUALIZATIONS
# ============================================================================

create_outcome_plots <- function(data, output_dir = "plots") {
  # Create comprehensive visualization plots

  dir.create(output_dir, showWarnings = FALSE)

  metrics <- c("pain_level", "sleep_quality", "fatigue_level",
               "anxiety_level", "function_level")

  metric_labels <- c(
    pain_level = "Pain Level (0-10)",
    sleep_quality = "Sleep Quality (0-10)",
    fatigue_level = "Fatigue Level (0-10)",
    anxiety_level = "Anxiety Level (0-10)",
    function_level = "Function Level (0-10)"
  )

  plots <- list()

  for (metric in metrics) {
    # Weekly trend plot with confidence intervals
    p <- ggplot(data %>% filter(!is.na(!!sym(metric))),
                aes(x = week, y = !!sym(metric))) +
      stat_summary(fun = mean, geom = "line", size = 1.2, color = "#4A90E2") +
      stat_summary(fun = mean, geom = "point", size = 3, color = "#4A90E2") +
      stat_summary(fun.data = mean_cl_normal, geom = "errorbar",
                   width = 0.2, color = "#4A90E2", alpha = 0.6) +
      labs(
        title = paste("Weekly Trend:", metric_labels[[metric]]),
        x = "Week",
        y = metric_labels[[metric]],
        subtitle = "Mean ± 95% CI"
      ) +
      theme_minimal() +
      theme(
        plot.title = element_text(size = 14, face = "bold"),
        plot.subtitle = element_text(size = 10, color = "gray40"),
        panel.grid.minor = element_blank()
      ) +
      scale_x_continuous(breaks = 1:8)

    plots[[metric]] <- p

    # Save plot
    ggsave(file.path(output_dir, paste0(metric, "_trend.png")),
           plot = p, width = 8, height = 5, dpi = 300)
  }

  # Create combined plot
  combined_plot <- grid.arrange(grobs = plots, ncol = 2)
  ggsave(file.path(output_dir, "all_metrics_trends.png"),
         plot = combined_plot, width = 12, height = 15, dpi = 300)

  return(plots)
}

create_change_barplot <- function(ttest_results, output_path = "change_barplot.png") {
  # Create bar plot showing pre-post changes

  changes_df <- data.frame(
    metric = names(ttest_results),
    mean_change = sapply(ttest_results, function(x) x$mean_change),
    ci_lower = sapply(ttest_results, function(x) x$ci_lower),
    ci_upper = sapply(ttest_results, function(x) x$ci_upper),
    p_value = sapply(ttest_results, function(x) x$p_value)
  )

  changes_df$significant <- changes_df$p_value < 0.05

  p <- ggplot(changes_df, aes(x = reorder(metric, mean_change),
                              y = mean_change, fill = significant)) +
    geom_col(width = 0.7) +
    geom_errorbar(aes(ymin = ci_lower, ymax = ci_upper),
                  width = 0.2, size = 0.8) +
    geom_hline(yintercept = 0, linetype = "dashed", color = "gray50") +
    scale_fill_manual(values = c("TRUE" = "#2ECC71", "FALSE" = "#E74C3C"),
                      labels = c("TRUE" = "p < 0.05", "FALSE" = "n.s.")) +
    coord_flip() +
    labs(
      title = "Pre-Post Changes in Outcome Metrics",
      subtitle = "Mean change from Week 1 to Week 8 (with 95% CI)",
      x = "",
      y = "Mean Change",
      fill = "Statistical\nSignificance"
    ) +
    theme_minimal() +
    theme(
      plot.title = element_text(size = 14, face = "bold"),
      legend.position = "top"
    )

  ggsave(output_path, plot = p, width = 8, height = 6, dpi = 300)

  return(p)
}

# ============================================================================
# 8. REPORT GENERATION
# ============================================================================

generate_statistical_report <- function(data, output_path = "statistical_report.html") {
  # Generate comprehensive HTML report

  cat("# Pain Management Program Statistical Analysis Report\n\n")
  cat("Generated:", format(Sys.time(), "%Y-%m-%d %H:%M:%S"), "\n\n")

  # Calculate all analyses
  descriptive <- calculate_descriptive_stats(data)
  ttests <- perform_paired_ttests(data)
  anova_results <- perform_repeated_measures_anova(data)
  longitudinal <- fit_longitudinal_models(data)
  clinical_sig <- calculate_clinical_significance(data)

  # Create visualizations
  plots <- create_outcome_plots(data)
  change_plot <- create_change_barplot(ttests)

  # Print results
  cat("## Summary Statistics\n\n")
  print(kable(descriptive))

  cat("\n## Paired T-Tests (Week 1 vs Week 8)\n\n")
  print(kable(ttests))

  cat("\n## Clinical Significance\n\n")
  print(kable(clinical_sig))

  cat("\n## Program Effectiveness\n")
  cat("- Statistically significant improvements in",
      sum(sapply(ttests, function(x) x$p_value < 0.05)), "out of 5 metrics\n")
  cat("- Clinically significant improvements in",
      sum(sapply(clinical_sig, function(x) x$percentage_improved > 50)),
      "out of 5 metrics\n")

  return(list(
    descriptive = descriptive,
    ttests = ttests,
    anova = anova_results,
    longitudinal = longitudinal,
    clinical_significance = clinical_sig
  ))
}

# ============================================================================
# 9. MAIN EXECUTION
# ============================================================================

main <- function(data_path = "../data/patient_outcomes.csv") {
  # Main analysis pipeline

  cat("Loading data...\n")
  data <- load_patient_data(data_path)
  data <- calculate_week_number(data)

  cat("Running statistical analyses...\n")
  results <- generate_statistical_report(data)

  cat("\nAnalysis complete! Results saved.\n")

  return(results)
}

# Run if executed as script
if (!interactive()) {
  results <- main()
}
