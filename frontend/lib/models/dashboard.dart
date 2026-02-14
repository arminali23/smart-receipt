class DailySpending {
  final String date;
  final double total;

  DailySpending({required this.date, required this.total});

  factory DailySpending.fromJson(Map<String, dynamic> json) {
    return DailySpending(
      date: json['date'],
      total: (json['total'] as num).toDouble(),
    );
  }
}

class CategorySpending {
  final String category;
  final double total;

  CategorySpending({required this.category, required this.total});

  factory CategorySpending.fromJson(Map<String, dynamic> json) {
    return CategorySpending(
      category: json['category'],
      total: (json['total'] as num).toDouble(),
    );
  }
}

class DashboardData {
  final List<DailySpending> dailySpending;
  final List<DailySpending> monthlySpending;
  final List<CategorySpending> categorySpending;
  final int totalReceipts;
  final double totalSpent;

  DashboardData({
    required this.dailySpending,
    required this.monthlySpending,
    required this.categorySpending,
    required this.totalReceipts,
    required this.totalSpent,
  });

  factory DashboardData.fromJson(Map<String, dynamic> json) {
    return DashboardData(
      dailySpending: (json['daily_spending'] as List)
          .map((e) => DailySpending.fromJson(e))
          .toList(),
      monthlySpending: (json['monthly_spending'] as List)
          .map((e) => DailySpending.fromJson(e))
          .toList(),
      categorySpending: (json['category_spending'] as List)
          .map((e) => CategorySpending.fromJson(e))
          .toList(),
      totalReceipts: json['total_receipts'],
      totalSpent: (json['total_spent'] as num).toDouble(),
    );
  }
}
