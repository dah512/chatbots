#!/usr/bin/env Rscript
# Comprehensive Analysis of Pain Management Program Simulation Results
# Analyzes the simulated 8-week program outcomes for 25 diverse patients

library(jsonlite)
library(ggplot2)
library(dplyr)
library(tidyr)
library(gridExtra)

# Set working directory to script location
setwd(dirname(sys.frame(1)$ofile))

# Read simulation data
cat("Loading simulation data...\n")
pain_logs <- fromJSON("../python/program_simulation_pain_logs.json")
assessments <- fromJSON("../python/program_simulation_assessments.json")
outcomes <- fromJSON("../python/program_outcomes_report.json")
profiles <- fromJSON("../python/cohort_profiles.json")

# ============================================================================
# 1. PAIN TRAJECTORY ANALYSIS
# ============================================================================

# Convert pain logs to data frame
pain_df <- do.call(rbind, lapply(names(pain_logs), function(patient_id) {
  patient_logs <- pain_logs[[patient_id]]
  do.call(rbind, lapply(patient_logs, function(log) {
    data.frame(
      patient_id = patient_id,
      log_date = log$log_date,
      pain_level = log$pain_level,
      sleep_quality = log$sleep_quality,
      fatigue_level = log$fatigue_level,
      anxiety_level = log$anxiety_level,
      function_level = log$function_level,
      stringsAsFactors = FALSE
    )
  }))
}))

# Add week number
pain_df$log_date <- as.Date(pain_df$log_date)
pain_df <- pain_df %>%
  group_by(patient_id) %>%
  mutate(
    day_number = as.numeric(log_date - min(log_date)) + 1,
    week_number = ceiling(day_number / 7)
  ) %>%
  ungroup()

# Calculate weekly averages
weekly_avg <- pain_df %>%
  group_by(patient_id, week_number) %>%
  summarise(
    avg_pain = mean(pain_level, na.rm = TRUE),
    avg_sleep = mean(sleep_quality, na.rm = TRUE),
    avg_fatigue = mean(fatigue_level, na.rm = TRUE),
    avg_anxiety = mean(anxiety_level, na.rm = TRUE),
    avg_function = mean(function_level, na.rm = TRUE),
    .groups = "drop"
  )

# ============================================================================
# 2. STATISTICAL TESTS
# ============================================================================

cat("\n========================================\n")
cat("STATISTICAL ANALYSIS OF SIMULATION DATA\n")
cat("========================================\n\n")

# Paired t-tests: Week 1 vs Week 8
week1 <- weekly_avg %>% filter(week_number == 1)
week8 <- weekly_avg %>% filter(week_number == 8)

# Merge for paired analysis
paired_data <- inner_join(week1, week8, by = "patient_id", suffix = c("_w1", "_w8"))

metrics <- c("pain", "sleep", "fatigue", "anxiety", "function")
ttest_results <- list()

for (metric in metrics) {
  w1_col <- paste0("avg_", metric, "_w1")
  w8_col <- paste0("avg_", metric, "_w8")

  if (w1_col %in% names(paired_data) && w8_col %in% names(paired_data)) {
    w1_vals <- paired_data[[w1_col]]
    w8_vals <- paired_data[[w8_col]]

    # Remove NA values
    valid_idx <- !is.na(w1_vals) & !is.na(w8_vals)
    w1_vals <- w1_vals[valid_idx]
    w8_vals <- w8_vals[valid_idx]

    if (length(w1_vals) > 1) {
      t_test <- t.test(w8_vals, w1_vals, paired = TRUE)
      mean_change <- mean(w8_vals - w1_vals)
      sd_change <- sd(w8_vals - w1_vals)

      # Cohen's d for paired samples
      cohens_d <- mean_change / sd_change

      ttest_results[[metric]] <- list(
        mean_w1 = mean(w1_vals),
        mean_w8 = mean(w8_vals),
        mean_change = mean_change,
        sd_change = sd_change,
        t_statistic = t_test$statistic,
        p_value = t_test$p.value,
        ci_lower = t_test$conf.int[1],
        ci_upper = t_test$conf.int[2],
        cohens_d = cohens_d,
        n = length(w1_vals)
      )

      cat(sprintf("%s:\n", toupper(metric)))
      cat(sprintf("  Week 1 Mean: %.2f\n", mean(w1_vals)))
      cat(sprintf("  Week 8 Mean: %.2f\n", mean(w8_vals)))
      cat(sprintf("  Mean Change: %.2f (SD = %.2f)\n", mean_change, sd_change))
      cat(sprintf("  t-statistic: %.3f\n", t_test$statistic))
      cat(sprintf("  p-value: %.4f %s\n", t_test$p.value,
                  ifelse(t_test$p.value < 0.05, "**", "")))
      cat(sprintf("  95%% CI: [%.2f, %.2f]\n", t_test$conf.int[1], t_test$conf.int[2]))
      cat(sprintf("  Cohen's d: %.3f (%s)\n\n", cohens_d,
                  ifelse(abs(cohens_d) < 0.2, "negligible",
                         ifelse(abs(cohens_d) < 0.5, "small",
                                ifelse(abs(cohens_d) < 0.8, "medium", "large")))))
    }
  }
}

# ============================================================================
# 3. KNOWLEDGE ASSESSMENT ANALYSIS
# ============================================================================

cat("\n========================================\n")
cat("KNOWLEDGE ASSESSMENT RESULTS\n")
cat("========================================\n\n")

# Convert assessments to data frame
assessment_df <- do.call(rbind, lapply(names(assessments), function(patient_id) {
  patient_assessments <- assessments[[patient_id]]
  do.call(rbind, lapply(patient_assessments, function(assessment) {
    data.frame(
      patient_id = patient_id,
      week = assessment$week,
      assessment_type = assessment$assessment_type,
      score = assessment$score,
      total_points = assessment$total_points,
      percentage = assessment$percentage,
      stringsAsFactors = FALSE
    )
  }))
}))

# Calculate knowledge gains
knowledge_gains <- assessment_df %>%
  pivot_wider(
    id_cols = c(patient_id, week),
    names_from = assessment_type,
    values_from = percentage
  ) %>%
  mutate(
    knowledge_gain = post - pre
  ) %>%
  filter(!is.na(knowledge_gain))

cat(sprintf("Average Knowledge Gain per Week: %.2f%%\n",
            mean(knowledge_gains$knowledge_gain, na.rm = TRUE)))
cat(sprintf("SD: %.2f%%\n", sd(knowledge_gains$knowledge_gain, na.rm = TRUE)))
cat(sprintf("Range: %.2f%% to %.2f%%\n\n",
            min(knowledge_gains$knowledge_gain, na.rm = TRUE),
            max(knowledge_gains$knowledge_gain, na.rm = TRUE)))

# Overall knowledge gain (first pre-test to last post-test)
first_pre <- assessment_df %>%
  filter(assessment_type == "pre") %>%
  group_by(patient_id) %>%
  filter(week == min(week)) %>%
  select(patient_id, pre_score = percentage)

last_post <- assessment_df %>%
  filter(assessment_type == "post") %>%
  group_by(patient_id) %>%
  filter(week == max(week)) %>%
  select(patient_id, post_score = percentage)

overall_gain <- inner_join(first_pre, last_post, by = "patient_id") %>%
  mutate(overall_gain = post_score - pre_score)

cat("Overall Program Knowledge Gain (Week 1 Pre to Week 8 Post):\n")
cat(sprintf("  Mean: %.2f%%\n", mean(overall_gain$overall_gain, na.rm = TRUE)))
cat(sprintf("  Median: %.2f%%\n", median(overall_gain$overall_gain, na.rm = TRUE)))
cat(sprintf("  SD: %.2f%%\n\n", sd(overall_gain$overall_gain, na.rm = TRUE)))

# ============================================================================
# 4. VISUALIZATIONS
# ============================================================================

cat("Generating visualizations...\n")

# Create output directory for plots
dir.create("simulation_plots", showWarnings = FALSE)

# Plot 1: Individual Pain Trajectories
p1 <- ggplot(weekly_avg, aes(x = week_number, y = avg_pain, group = patient_id)) +
  geom_line(alpha = 0.3, color = "steelblue") +
  geom_smooth(aes(group = 1), method = "loess", se = TRUE, color = "red", size = 1.5) +
  labs(
    title = "Individual Pain Trajectories Over 8 Weeks",
    subtitle = "Red line shows average trend across all patients",
    x = "Week Number",
    y = "Average Pain Level (0-10)"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(face = "bold", size = 14))

ggsave("simulation_plots/01_pain_trajectories.png", p1, width = 10, height = 6, dpi = 300)

# Plot 2: Week 1 vs Week 8 Pain Comparison
comparison_data <- paired_data %>%
  select(patient_id, avg_pain_w1, avg_pain_w8) %>%
  pivot_longer(cols = c(avg_pain_w1, avg_pain_w8),
               names_to = "timepoint",
               values_to = "pain_level") %>%
  mutate(timepoint = ifelse(timepoint == "avg_pain_w1", "Week 1", "Week 8"))

p2 <- ggplot(comparison_data, aes(x = timepoint, y = pain_level)) +
  geom_boxplot(fill = c("lightcoral", "lightgreen"), alpha = 0.7) +
  geom_line(aes(group = patient_id), alpha = 0.2) +
  geom_point(alpha = 0.5) +
  labs(
    title = "Pain Levels: Week 1 vs Week 8",
    subtitle = "Lines connect individual patients",
    x = "",
    y = "Pain Level (0-10)"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(face = "bold", size = 14))

ggsave("simulation_plots/02_pain_comparison_boxplot.png", p2, width = 8, height = 6, dpi = 300)

# Plot 3: Multi-metric Dashboard
metrics_long <- weekly_avg %>%
  select(patient_id, week_number, starts_with("avg_")) %>%
  pivot_longer(cols = starts_with("avg_"),
               names_to = "metric",
               values_to = "value") %>%
  mutate(
    metric = gsub("avg_", "", metric),
    metric = factor(metric, levels = c("pain", "fatigue", "anxiety", "sleep", "function"),
                   labels = c("Pain", "Fatigue", "Anxiety", "Sleep Quality", "Function"))
  )

p3 <- ggplot(metrics_long, aes(x = week_number, y = value)) +
  geom_jitter(alpha = 0.1, width = 0.2, color = "gray50") +
  geom_smooth(method = "loess", se = TRUE, color = "darkblue", fill = "lightblue") +
  facet_wrap(~metric, ncol = 2, scales = "free_y") +
  labs(
    title = "All Outcome Metrics Over 8 Weeks",
    subtitle = "Trends show population averages with 95% confidence intervals",
    x = "Week Number",
    y = "Score (0-10)"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    strip.text = element_text(face = "bold", size = 11)
  )

ggsave("simulation_plots/03_all_metrics_dashboard.png", p3, width = 12, height = 10, dpi = 300)

# Plot 4: Knowledge Assessment Progress
p4 <- ggplot(knowledge_gains, aes(x = factor(week), y = knowledge_gain)) +
  geom_boxplot(fill = "lightblue", alpha = 0.7) +
  geom_jitter(alpha = 0.3, width = 0.2) +
  geom_hline(yintercept = 0, linetype = "dashed", color = "red") +
  labs(
    title = "Knowledge Gain by Week (Post-test minus Pre-test)",
    x = "Week Number",
    y = "Knowledge Gain (%)"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(face = "bold", size = 14))

ggsave("simulation_plots/04_knowledge_gains.png", p4, width = 10, height = 6, dpi = 300)

# Plot 5: Responder Analysis
responder_data <- paired_data %>%
  mutate(
    pain_change = avg_pain_w8 - avg_pain_w1,
    responder_status = case_when(
      pain_change <= -2 ~ "Strong Responder (≥2 pt decrease)",
      pain_change < 0 ~ "Modest Responder (decreased)",
      pain_change == 0 ~ "No Change",
      TRUE ~ "Non-Responder (increased)"
    )
  )

responder_counts <- responder_data %>%
  count(responder_status) %>%
  mutate(percentage = n / sum(n) * 100)

p5 <- ggplot(responder_counts, aes(x = reorder(responder_status, -n), y = n, fill = responder_status)) +
  geom_bar(stat = "identity", alpha = 0.8) +
  geom_text(aes(label = sprintf("n=%d\n(%.1f%%)", n, percentage)),
            vjust = -0.5, size = 4) +
  scale_fill_manual(values = c(
    "Strong Responder (≥2 pt decrease)" = "darkgreen",
    "Modest Responder (decreased)" = "lightgreen",
    "No Change" = "gray",
    "Non-Responder (increased)" = "lightcoral"
  )) +
  labs(
    title = "Patient Response Classification",
    subtitle = "Based on pain level change from Week 1 to Week 8",
    x = "",
    y = "Number of Patients"
  ) +
  theme_minimal() +
  theme(
    plot.title = element_text(face = "bold", size = 14),
    legend.position = "none",
    axis.text.x = element_text(angle = 15, hjust = 1)
  )

ggsave("simulation_plots/05_responder_analysis.png", p5, width = 10, height = 6, dpi = 300)

# Plot 6: Correlation between baseline and improvement
responder_data_with_baseline <- responder_data %>%
  mutate(baseline_pain = avg_pain_w1)

p6 <- ggplot(responder_data_with_baseline, aes(x = baseline_pain, y = -pain_change)) +
  geom_point(size = 3, alpha = 0.6, color = "steelblue") +
  geom_smooth(method = "lm", se = TRUE, color = "red") +
  labs(
    title = "Baseline Pain vs Pain Reduction",
    subtitle = "Higher baseline pain associated with greater improvement potential",
    x = "Baseline Pain Level (Week 1)",
    y = "Pain Reduction (points)"
  ) +
  theme_minimal() +
  theme(plot.title = element_text(face = "bold", size = 14))

ggsave("simulation_plots/06_baseline_vs_improvement.png", p6, width = 8, height = 6, dpi = 300)

# ============================================================================
# 5. EXPORT SUMMARY REPORT
# ============================================================================

summary_report <- list(
  simulation_info = list(
    n_patients = nrow(paired_data),
    simulation_date = Sys.Date(),
    analysis_version = "1.0"
  ),
  pain_outcomes = ttest_results$pain,
  other_outcomes = ttest_results[names(ttest_results) != "pain"],
  knowledge_outcomes = list(
    mean_weekly_gain = mean(knowledge_gains$knowledge_gain, na.rm = TRUE),
    overall_mean_gain = mean(overall_gain$overall_gain, na.rm = TRUE),
    overall_median_gain = median(overall_gain$overall_gain, na.rm = TRUE)
  ),
  responder_analysis = list(
    strong_responders = sum(responder_data$pain_change <= -2),
    modest_responders = sum(responder_data$pain_change < 0 & responder_data$pain_change > -2),
    no_change = sum(responder_data$pain_change == 0),
    non_responders = sum(responder_data$pain_change > 0),
    improvement_rate = sum(responder_data$pain_change < 0) / nrow(responder_data) * 100
  )
)

write_json(summary_report, "simulation_statistical_summary.json",
           pretty = TRUE, auto_unbox = TRUE)

cat("\n========================================\n")
cat("ANALYSIS COMPLETE\n")
cat("========================================\n\n")
cat("Generated 6 visualization plots in simulation_plots/\n")
cat("Exported statistical summary to simulation_statistical_summary.json\n\n")

cat("Key Findings:\n")
cat(sprintf("- %d patients completed simulation\n", nrow(paired_data)))
cat(sprintf("- Mean pain reduction: %.2f points (p = %.4f)\n",
            ttest_results$pain$mean_change, ttest_results$pain$p_value))
cat(sprintf("- Effect size (Cohen's d): %.3f\n", ttest_results$pain$cohens_d))
cat(sprintf("- Improvement rate: %.1f%%\n", summary_report$responder_analysis$improvement_rate))
cat(sprintf("- Mean knowledge gain: %.2f%%\n",
            summary_report$knowledge_outcomes$overall_mean_gain))
cat("\nAll results saved successfully.\n")
