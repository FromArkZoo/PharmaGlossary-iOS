import SwiftUI

struct TermDetailView: View {
    @EnvironmentObject var store: GlossaryStore
    let term: Term

    var body: some View {
        ZStack {
            PGBackground()
            ScrollView {
                VStack(alignment: .leading, spacing: 14) {
                    header
                    if term.hasSnappy {
                        snappy
                    }
                    definition
                    tags
                    if term.hasSources {
                        sourcesFooter
                    }
                    Spacer(minLength: 24)
                }
                .padding(.horizontal, 16)
                .padding(.top, 8)
            }
        }
        .navigationTitle(term.term)
        .navigationBarTitleDisplayMode(.inline)
        .toolbar {
            ToolbarItem(placement: .topBarTrailing) {
                Button {
                    store.toggleFavorite(term)
                } label: {
                    Image(systemName: store.isFavorited(term) ? "star.fill" : "star")
                        .font(.system(size: 19, weight: .semibold))
                        .foregroundStyle(PGColors.accent)
                }
                .accessibilityLabel(store.isFavorited(term) ? "Remove from favorites" : "Add to favorites")
            }
        }
    }

    private var header: some View {
        VStack(alignment: .leading, spacing: 4) {
            if term.hasCategory {
                Text(term.category)
                    .font(PGFont.eyebrow)
                    .tracking(1.6)
                    .textCase(.uppercase)
                    .foregroundStyle(PGColors.accent)
                    .padding(.top, 14)
            }
            Text(term.term)
                .font(PGFont.termTitle)
                .foregroundStyle(PGColors.ink)
                .lineLimit(2)
                .minimumScaleFactor(0.7)
                .padding(.top, 2)
            if term.hasFull {
                Text(term.full)
                    .font(PGFont.termFullItalic)
                    .foregroundStyle(PGColors.inkLight)
                    .padding(.top, 2)
            }
            Rectangle()
                .fill(PGColors.inkRule)
                .frame(height: 1)
                .padding(.top, 12)
        }
    }

    private var snappy: some View {
        Text(term.snappy)
            .font(PGFont.snappyItalic)
            .foregroundStyle(PGColors.accent)
            .fixedSize(horizontal: false, vertical: true)
            .padding(.leading, 14)
            .frame(maxWidth: .infinity, alignment: .leading)
            .overlay(alignment: .leading) {
                Rectangle()
                    .fill(PGColors.accent)
                    .frame(width: 2)
            }
            .padding(.top, 2)
            .padding(.bottom, 6)
    }

    private var definition: some View {
        VStack(alignment: .leading, spacing: 8) {
            Text("Definition")
                .font(PGFont.eyebrow)
                .tracking(2)
                .textCase(.uppercase)
                .foregroundStyle(PGColors.inkLight)
            Text(store.attributedDetail(for: term))
                .font(PGFont.body)
                .foregroundStyle(PGColors.ink)
                .lineSpacing(3)
                .frame(maxWidth: .infinity, alignment: .leading)
        }
    }

    @ViewBuilder
    private var tags: some View {
        let chips = tagLabels
        if !chips.isEmpty {
            HStack(spacing: 6) {
                ForEach(chips, id: \.self) { label in
                    Text(label.uppercased())
                        .font(.system(size: 10, weight: .semibold))
                        .tracking(0.6)
                        .foregroundStyle(PGColors.accent)
                        .padding(.horizontal, 8)
                        .padding(.vertical, 3)
                        .overlay(
                            Capsule().stroke(PGColors.accent, lineWidth: 1)
                        )
                }
                Spacer()
            }
            .padding(.top, 6)
        }
    }

    private var tagLabels: [String] {
        var labels: [String] = []
        if term.hasCategory { labels.append(term.category) }
        labels.append(contentsOf: term.indications.prefix(2))
        return labels
    }

    private var sourcesFooter: some View {
        Text("Source: \(term.sources.joined(separator: ", "))")
            .font(.system(size: 11, weight: .regular, design: .serif).italic())
            .foregroundStyle(PGColors.inkFaint)
            .padding(.horizontal, 4)
            .padding(.top, 6)
    }

}
