clear

%Set the seed number
rng(100)

%Set data path
data_path = "Data/";

%Problem 2

%Load designated data
df = readtable(data_path+"A1_data.xlsx");

%Extract data variables
date = df.date;
nGDP = df.GDP;
nGPDI = df.GPDI;
nPCE = df.PCE;
CPI = df.CPI;
STIR = df.STIR;
LTIR = df.LTIR;

%P1 Q2
rGDP = nGDP./CPI*100;
rPCE = nPCE./CPI*100;
rGPDI = nGPDI./CPI*100;

%P1 Q3
% rGDP
figure(1);
plot(date, rGDP);
xlabel('Time');
ylabel('rGDP');
title('P1 Q3 - RGDP');
grid on;

% rPCE
figure(2);
plot(date, rPCE);
xlabel('Time');
ylabel('rPCE');
title('P1 Q3 - rPCE');
grid on;

% rGPDI
figure(3);
plot(date, rGPDI);
xlabel('Time');
ylabel('rGPDI');
title('P1 Q3 - rGPDI');
grid on;

% P1 Q4
rGDP_shifted1 = [NaN(4,1); rGDP(1:end-4)]; % shift data in order to calculate YoY growth (we lose first 4 quarters)
rGDPYoY = (rGDP - rGDP_shifted1) ./ rGDP_shifted1 * 100;
rGDPYoY(1:4, :) = []; % remove the first four NaN values

rGDP_shifted2 = [NaN(1,1); rGDP(1:end-1)]; % shift data in order to calculate QoQ growth (we lose first quarter)
rGDPQoQ = (rGDP - rGDP_shifted2) ./ rGDP_shifted2 * 100;
rGDPQoQ(1:1, :) = []; % remove the NaN value

Ldetrend = detrend(rGDP, 'linear');

HPdetrend = hpfilter(rGDP, 1600);
rGDP_HPdetrend = rGDP-HPdetrend;

%P1 Q5
figure(4)
yyaxis left
plot(date(5:end),rGDPYoY,date(5:end),rGDPQoQ(4:end))
hold on;
ylabel('Growth Rates')
yyaxis right
plot(date(5:end), Ldetrend(5:174), date(5:end), rGDP_HPdetrend(5:174))
ylim([-1700 1700])
ylabel ('Trends')
legend('YoY growth','QoQ growth', 'Linear trend','HP trend')
grid on
xlabel ('Year')

%P2 Q6
last_quarter_row = 167;

ln_rGDP = log(rGDP);
ln_rGDP_shifted = log(rGDP_shifted2);
lndiff_rGDP = ln_rGDP(2:end) - ln_rGDP_shifted(2:end);
lndiff_rGDP = lndiff_rGDP(1:last_quarter_row);

%P2 Q7
y = lndiff_rGDP(2:end);
y_lag1 = [ones(last_quarter_row-1, 1), lndiff_rGDP(1:end-1)];

phi_hat = y_lag1\y;

%P2 Q9
%First
IRF1 = ones(20,1);
y_0 = 1;

for t = 1:20

    if t == 1
        y = phi_hat(1,1) + phi_hat(2,1)*y_0; % y_0 is given by 1
    else
        y = phi_hat(1,1) + phi_hat(2,1)*IRF1(t-1);
    end

    IRF1(t) = y;
end

%Second
IRF2 = ones(20,1);

for t = 1:20

    if t == 1
        y = phi_hat(1,1) + phi_hat(2,1)*y_0 + 1; % y_t-1 is given by 1 and e_t is given by 1
    else
        y = phi_hat(1,1) + phi_hat(2,1)*IRF2(t-1);
    end

    IRF2(t) = y;
end

%Define periods
t = 1:20;

figure(5)
plot (t,IRF1)
xlabel ('t')
ylabel ('IRF1')
title ('IRF without shock')

figure(6)
plot (t,IRF2)
xlabel ('t')
ylabel ('IRF2')
title ('IRF with shock at time t')

%P2 Q10
IRF3 = IRF2-IRF1;

figure(7)
plot (t,IRF3)
xlabel ('t')
ylabel ('IRF3')
title ('IRF as deviation from baseline')


%P2 Q11
Log_CPI=log(CPI);
LogDiff_CPI = Log_CPI(2:168) - Log_CPI(1:167);

%P2 Q12
%%%%%%Add Interst rate too
lag = 1;

%Set variables
LogDiff_CPI_current_var1 = LogDiff_CPI(lag+1:end, :);

LogDiff_CPI_lag1 = lagmatrix(LogDiff_CPI, 1:lag);
LogDiff_CPI_lag1 = LogDiff_CPI_lag1(2:end, :);

X_lag1=[ones(166,1), LogDiff_CPI_lag1];

B_hat1 = X_lag1\LogDiff_CPI_lag1;

%P2 Q13
%Set variables
constant_var1 = ones(166,1);
STIR_current = STIR(1:167);
STIR_current_var1 = STIR_current(lag+1:end);
STIR_lag1 = lagmatrix(STIR_current, 1:lag);
STIR_lag1 = STIR_lag1(lag+1:end, :);

%Stack the variables
Y_t_var1 = [LogDiff_CPI_current_var1, STIR_current_var1];
X_t_var1 = [constant_var1, LogDiff_CPI_lag1, STIR_lag1];

%P2 Q14
B_hat_var1 = X_t_var1\Y_t_var1;

%P2 Q15
%%%%%Need to plot
Y_hat_var1 = X_t_var1*B_hat_var1;
residuals_var1 = Y_t_var1 - Y_hat_var1;
residual_CPI_var1 = residuals_var1(:,1);
residual_STIR_var1 = residuals_var1(:,2);

t = date(2:167);

figure (8)
subplot (2,1,1), plot (t, residual_CPI_var1)
title ('VAR(1) residuals')
xlabel ('Date')
ylabel ('Residuals of Log Difference CPI of VAR(1)')
subplot (2,1,2), plot (t, residual_STIR_var1)
xlabel ('Date')
ylabel ('Residuals of Short Term Interest Rate of VAR(1)')
%Doesn't hold the homoskeasticity assumption as they seem to have different
%variances.

%P2 Q16
mat_cov_var1 = cov([residual_CPI_var1, residual_STIR_var1]);

%P2 Q17
%Build variables for VAR(4)
lags = 4;

constant_var4 = ones(163, 1);

LogDiff_CPI_lag4 = lagmatrix(LogDiff_CPI, 1:lags);
LogDiff_CPI_lag4 = LogDiff_CPI_lag4(lags+1:end, :);
STIR_lag4 = lagmatrix(STIR_current, 1:lags);
STIR_lag4 = STIR_lag4(lags+1:end, :);

LogDiff_CPI_current_var4 = LogDiff_CPI(lags+1:end, :);
STIR_current_var4 = STIR_current(lags+1:end, :);

Y_t_var4 = [LogDiff_CPI_current_var4, STIR_current_var4];
X_t_var4 = [constant_var4, LogDiff_CPI_lag4, STIR_lag4];

%Regression
B_hat_var4 = X_t_var4\Y_t_var4;%Why do the coefficents have alternations of signs on every period?

%Residuals
Y_hat_var4 = X_t_var4*B_hat_var4;
residuals_var4 = Y_t_var4 - Y_hat_var4;
residual_CPI_var4 = residuals_var4(:,1);
residual_STIR_var4 = residuals_var4(:,2);

%Plot
t = date(5:167);

figure (9)
subplot (2,1,1), plot (t, residual_CPI_var4)
title ('VAR(4) residuals')
xlabel ('Date')
ylabel ('Residuals of Log Difference CPI of VAR(4)')
subplot (2,1,2), plot (t, residual_STIR_var4)
xlabel ('Date')
ylabel ('Residuals of Short Term Interest Rate of VAR(4)')

%P2 Q18
mat_cov_var4 = cov([residual_CPI_var4, residual_STIR_var4]);

%P2 Q19
%%%%%Must have modifications for this
%Number of variables
n_var1 = 2*(1 + 2*1);
n_var4 = 2*(1 + 2*4);

%Criterion for VAR(1)
AIC_var1 = log(det(mat_cov_var1)) + 2*n_var1^2/166;
BIC_var1 = log(det(mat_cov_var1)) + n_var1^2/166*log(166);
HQ_var1 = log(det(mat_cov_var1)) + 2*n_var1^2/166*log(log(166));
Vec_var1 = [AIC_var1, BIC_var1, HQ_var1]';

%Criterion for VAR(4)
AIC_var4 = log(det(mat_cov_var4)) + 2*n_var4^2*4/163;
BIC_var4 = log(det(mat_cov_var4)) + n_var4^2*4/163*log(163);
HQ_var4 = log(det(mat_cov_var4)) + 2*n_var4^2*4/163*log(log(163));
Vec_var4 = [AIC_var4, BIC_var4, HQ_var4]';

%Merge
Vec_cri = [Vec_var1, Vec_var4];

%%%%%%%
%%%%%%%
% n_VAR1=2*(1 + 2*1); % parameters to estimate
% T_VAR1=166; % observations
% p_VAR1=1; % lags
% det_VAR1= det(mat_cov_var4); % Determinant of sigma VAR(1)
% 
% n_VAR4=2*(1 + 2*4); % parameters to estimate
% T_VAR4=163; % observations
% p_VAR4=4; % lags
% det_VAR4= det(mat_cov_var4); % Determinant of sigma VR(4)
% 
%     % HQC:
%     HQC_VAR1=det_VAR1+2*log(log(T_VAR1))*n_VAR1*n_VAR1*p_VAR1/T_VAR1
%     HQC_VAR4=det_VAR4+2*log(log(T_VAR4))*n_VAR4*n_VAR4*p_VAR4/T_VAR4
%     % AIC:
%     AIC_VAR1=det_VAR1+2*n_VAR1*p_VAR1/T_VAR1
%     AIC_VAR4=det_VAR4+2*n_VAR4*p_VAR4/T_VAR4
%     % BIC:
%     BIC_VAR1=det_VAR1+log(T_VAR1)*n_VAR1*n_VAR1*p_VAR1/T_VAR1
%     BIC_VAR4=det_VAR4+log(T_VAR4)*n_VAR4*n_VAR4*p_VAR4/T_VAR4
%%%%%%%%
%%%%%%%%

%P2 Q20
%%%%%Should they be separated or attached?
residuals_star_container = zeros(166, 2, 100);

for i = 1:100
    residuals_star = datasample(residuals_var1, 166);
    residuals_star_container(:, :, i) = residuals_star;
end

%P2 Q21
Y_star_container = zeros(166, 2, 100);

for i = 1:100
    Y_star_container(:, :, i) = X_t_var1*B_hat_var1 + residuals_star_container(:, :, i);
end

%P2 Q22
B_hat_star_container = zeros(3, 2, 100);

for i = 1:100
    B_hat_star_container(:, :, i) = X_t_var1\Y_star_container(:, :, i);
end

%P2 Q23
forecast_container = zeros(6, 2, 100);

for i = 1:100
    %First forecast
    forecast_container(1, :, i) = B_hat_star_container(1, :, i) + Y_t_var1(166, :) * B_hat_star_container(2:3, :, i);
    
    for j = 2:6
        %Following forecasts
        forecast_container(j, :, i) = B_hat_star_container(1, :, i) + forecast_container(j-1, :, i) * B_hat_star_container(2:3, :, i);
    end

end

inflation_forecasts = forecast_container(:, 1, :);

%P2 Q24
%Reshape the array of forecasts of inflation rate to a 100*6 matrix
mat_forecasts = reshape(permute(inflation_forecasts, [3, 1, 2]), 100, 6);

%Calculate arguments for CIs
sample_means = mean(mat_forecasts, 1);
stds = std(mat_forecasts, 1);

%Calculate CIs
z_90 = 1.645;
confidence_interval = zeros(2, 6);

for i = 1:6
    confidence_interval(1, i) =  sample_means(i) + z_90 * stds(i)/sqrt(100);
    confidence_interval(2, i) =  sample_means(i) - z_90 * stds(i)/sqrt(100);
end

median_var1 = median(mat_forecasts, 1);

%Merge median valeu below difference of log cpi
merge_var1 = [LogDiff_CPI; median_var1'];

t = date(2:end);
t_ci = date(end-5:end);

figure(10)
plot (t, merge_var1, t_ci, confidence_interval(1, :), t_ci, confidence_interval(2, :))
title ('VAR(4) residuals')
xlabel ('Date')
ylabel ('Residuals of Log Difference CPI of VAR(4)')


%As the parameters are not specified for random walk,
%we reasonably adapt 0 as mean and variances from original residuals.
forecast_rw = zeros(100, 6);

for i = 1:100
    forecast_rw(i, 1) = Y_t_var1(166, 1) + sqrt(mat_cov_var1(1,1))*randn(1);
    
    for j = 2:6
        forecast_rw(i, j) = forecast_rw(1, j-1) + sqrt(mat_cov_var1(1,1))*randn(1);
    end
end




