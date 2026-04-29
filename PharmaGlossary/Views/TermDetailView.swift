import SwiftUI

struct TermDetailView: View {
    let term: Term

    var body: some View {
        ZStack {
            PGColors.bg.ignoresSafeArea()
            ScrollView {
                VStack(alignment: .leading, spacing: 16) {
                    header
                    definitionCard
                    Spacer(minLength: 24)
                }
                .padding(.horizontal, 16)
                .padding(.top, 16)
            }
        }
        .navigationTitle(term.term)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                ShareLink(item: shareText) {
                    Image(systemName: "square.and.arrow.up")
                }
                .tint(PGColors.primary)
            }
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(term.term)
                .font(.system(size: 30, weight: .bold))
                .foregroundStyle(PGColors.text)
            if term.hasFull {
                Text(term.full)
                    .font(.system(size: 15, weight: .medium))
                    .foregroundStyle(PGColors.primary)
            }
            HStack(spacing: 6) {
                Text(term.letter)
                    .font(.system(size: 11, weight: .bold))
                    .foregroundStyle(.white)
                    .frame(width: 22, height: 22)
                    .background(PGColors.primary)
                    .clipShape(Circle())
                Text("Letter \(term.letter)")
                    .font(.system(size: 12, weight: .regular))
                    .foregroundStyle(PGColors.textLight)
            }
            .padding(.top, 4)
        }
    }

    private var definitionCard: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Definition")
                .font(.system(size: 11, weight: .semibold))
                .foregroundStyle(PGColors.textLight)
                .textCase(.uppercase)
                .tracking(0.5)
            Text(term.definition)
                .font(PGFont.definition)
                .foregroundStyle(PGColors.text)
                .fixedSize(horizontal: false, vertical: true)
        }
        .padding(20)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(
            RoundedRectangle(cornerRadius: 16, style: .continuous)
                .fill(PGColors.hover)
        )
    }

    private var shareText: String {
        var s = term.term
        if term.hasFull { s += " (\(term.full))" }
        s += "\n\n\(term.definition)"
        return s
    }
}
