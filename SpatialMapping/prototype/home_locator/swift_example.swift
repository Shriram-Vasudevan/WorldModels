// Swift example for iOS integration with Home Object Locator API
// This is example code - adapt to your SwiftUI/UIKit app

import Foundation
import UIKit

// MARK: - API Models

struct UploadResponse: Codable {
    let success: Bool
    let photoId: String
    let timestamp: String
    let extracted: ExtractedData
    let message: String

    enum CodingKeys: String, CodingKey {
        case success
        case photoId = "photo_id"
        case timestamp
        case extracted
        case message
    }
}

struct ExtractedData: Codable {
    let objects: [ExtractedObject]
    let locations: [ExtractedLocation]
    let relationships: [Relationship]
}

struct ExtractedObject: Codable {
    let name: String
    let description: String?
    let location: String?
    let confidence: Double?
}

struct ExtractedLocation: Codable {
    let name: String
    let description: String?
    let type: String?
}

struct Relationship: Codable {
    let object: String
    let relation: String
    let location: String
}

struct QueryResponse: Codable {
    let success: Bool
    let question: String
    let answer: String
    let timestamp: String
}

// MARK: - API Client

class HomeLocatorAPI {
    // Change this to your Mac's IP address or server URL
    static let baseURL = "http://192.168.1.100:5001"

    /// Upload a photo with optional note
    static func uploadPhoto(
        image: UIImage,
        note: String? = nil,
        completion: @escaping (Result<UploadResponse, Error>) -> Void
    ) {
        guard let url = URL(string: "\(baseURL)/upload") else {
            completion(.failure(NSError(domain: "Invalid URL", code: 0)))
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"

        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var body = Data()

        // Add image
        if let imageData = image.jpegData(compressionQuality: 0.8) {
            body.append("--\(boundary)\r\n".data(using: .utf8)!)
            body.append("Content-Disposition: form-data; name=\"image\"; filename=\"photo.jpg\"\r\n".data(using: .utf8)!)
            body.append("Content-Type: image/jpeg\r\n\r\n".data(using: .utf8)!)
            body.append(imageData)
            body.append("\r\n".data(using: .utf8)!)
        }

        // Add note if provided
        if let note = note {
            body.append("--\(boundary)\r\n".data(using: .utf8)!)
            body.append("Content-Disposition: form-data; name=\"note\"\r\n\r\n".data(using: .utf8)!)
            body.append("\(note)\r\n".data(using: .utf8)!)
        }

        body.append("--\(boundary)--\r\n".data(using: .utf8)!)
        request.httpBody = body

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(NSError(domain: "No data", code: 0)))
                return
            }

            do {
                let uploadResponse = try JSONDecoder().decode(UploadResponse.self, from: data)
                completion(.success(uploadResponse))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }

    /// Query where an object is located
    static func query(
        question: String,
        completion: @escaping (Result<QueryResponse, Error>) -> Void
    ) {
        guard let url = URL(string: "\(baseURL)/query") else {
            completion(.failure(NSError(domain: "Invalid URL", code: 0)))
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body = ["question": question]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(NSError(domain: "No data", code: 0)))
                return
            }

            do {
                let queryResponse = try JSONDecoder().decode(QueryResponse.self, from: data)
                completion(.success(queryResponse))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }
}

// MARK: - Usage Example in SwiftUI

/*
import SwiftUI

struct ContentView: View {
    @State private var selectedImage: UIImage?
    @State private var note: String = ""
    @State private var isUploading = false
    @State private var lastResponse: String = ""
    @State private var searchQuery: String = ""
    @State private var searchResult: String = ""

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                // Photo upload section
                VStack {
                    if let image = selectedImage {
                        Image(uiImage: image)
                            .resizable()
                            .scaledToFit()
                            .frame(height: 200)
                    } else {
                        Button("Take Photo") {
                            // Show camera
                        }
                        .buttonStyle(.borderedProminent)
                    }

                    TextField("Add a note (optional)", text: $note)
                        .textFieldStyle(.roundedBorder)
                        .padding()

                    Button(action: uploadPhoto) {
                        if isUploading {
                            ProgressView()
                        } else {
                            Text("Upload & Analyze")
                        }
                    }
                    .disabled(selectedImage == nil || isUploading)
                    .buttonStyle(.borderedProminent)
                }

                Divider()

                // Query section
                VStack {
                    TextField("Where are my keys?", text: $searchQuery)
                        .textFieldStyle(.roundedBorder)
                        .padding()

                    Button("Search") {
                        searchForObject()
                    }
                    .buttonStyle(.borderedProminent)

                    if !searchResult.isEmpty {
                        Text(searchResult)
                            .padding()
                            .background(Color.gray.opacity(0.1))
                            .cornerRadius(8)
                    }
                }

                Spacer()
            }
            .padding()
            .navigationTitle("🏠 Object Finder")
        }
    }

    func uploadPhoto() {
        guard let image = selectedImage else { return }

        isUploading = true

        HomeLocatorAPI.uploadPhoto(image: image, note: note.isEmpty ? nil : note) { result in
            DispatchQueue.main.async {
                isUploading = false

                switch result {
                case .success(let response):
                    lastResponse = response.message
                    selectedImage = nil
                    note = ""

                case .failure(let error):
                    lastResponse = "Error: \(error.localizedDescription)"
                }
            }
        }
    }

    func searchForObject() {
        HomeLocatorAPI.query(question: searchQuery) { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let response):
                    searchResult = response.answer

                case .failure(let error):
                    searchResult = "Error: \(error.localizedDescription)"
                }
            }
        }
    }
}
*/

// MARK: - Remember to:
// 1. Replace HomeLocatorAPI.baseURL with your server's IP
// 2. Add camera permissions to Info.plist:
//    - NSCameraUsageDescription
//    - NSPhotoLibraryUsageDescription
// 3. Handle image picker (UIImagePickerController or PhotosPicker)
