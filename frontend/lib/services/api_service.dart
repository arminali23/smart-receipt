import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import '../models/receipt.dart';
import '../models/dashboard.dart';

class ApiService {
  // Change this to your backend URL
  // For Android emulator use: http://10.0.2.2:8000
  // For iOS simulator use: http://localhost:8000
  // For physical device use your computer's local IP
  static const String baseUrl = 'http://localhost:8000/api';

  Future<Receipt> scanReceipt(File imageFile) async {
    final uri = Uri.parse('$baseUrl/receipts/scan');
    final request = http.MultipartRequest('POST', uri);
    request.files.add(
      await http.MultipartFile.fromPath('file', imageFile.path),
    );

    final streamedResponse = await request.send();
    final response = await http.Response.fromStream(streamedResponse);

    if (response.statusCode == 200) {
      return Receipt.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to scan receipt: ${response.body}');
    }
  }

  Future<List<Receipt>> getReceipts() async {
    final response = await http.get(Uri.parse('$baseUrl/receipts/'));

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return data.map((json) => Receipt.fromJson(json)).toList();
    } else {
      throw Exception('Failed to load receipts');
    }
  }

  Future<DashboardData> getDashboard() async {
    final response = await http.get(Uri.parse('$baseUrl/dashboard/'));

    if (response.statusCode == 200) {
      return DashboardData.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to load dashboard');
    }
  }

  Future<void> deleteReceipt(int id) async {
    final response = await http.delete(
      Uri.parse('$baseUrl/receipts/$id'),
    );
    if (response.statusCode != 200) {
      throw Exception('Failed to delete receipt');
    }
  }
}
