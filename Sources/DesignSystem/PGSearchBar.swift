import SwiftUI

struct PGSearchBar: View {
    @Binding var text: String
    var prompt: String = "Search terms, abbreviations, definitions"

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: "magnifyingglass")
                .font(.system(size: 18, weight: .medium))
                .foregroundStyle(PGColors.ink)

            TextField(prompt, text: $text)
                .font(PGFont.body)
                .foregroundStyle(PGColors.ink)
                .autocorrectionDisabled()
                .textInputAutocapitalization(.never)
                .submitLabel(.search)

            if !text.isEmpty {
                Button {
                    text = ""
                } label: {
                    Image(systemName: "xmark.circle.fill")
                        .font(.system(size: 16))
                        .foregroundStyle(PGColors.inkFaint)
                }
                .buttonStyle(.plain)
                .accessibilityLabel("Clear search")
            }
        }
        .padding(.horizontal, 18)
        .padding(.vertical, 14)
        .background(
            RoundedRectangle(cornerRadius: 32, style: .continuous)
                .fill(PGColors.card)
        )
        .overlay(
            RoundedRectangle(cornerRadius: 32, style: .continuous)
                .stroke(PGColors.cardBorder.opacity(0.4), lineWidth: 1)
        )
    }
}

#Preview {
    @Previewable @State var text = ""
    VStack(spacing: 16) {
        PGSearchBar(text: $text)
        PGSearchBar(text: .constant("FDA"))
    }
    .padding()
    .background(PGColors.bg)
}
