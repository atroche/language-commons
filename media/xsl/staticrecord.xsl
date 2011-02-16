<?xml version="1.0" encoding="UTF-8"?>
<!--

    Originally created by Gary Simons using XML Spy v4.4 for his
    Free-standing OLAC Metadata service.
    
    Haejoong Lee took a copy (dated on 15 May 2006) and slightly
    modified it to use for static record pages.

    Changes:
    2006-06-16  Haejoong Lee  <haejoong@ldc.upenn.edu>
      * first edition
          
-->
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:olac11="http://www.language-archives.org/OLAC/1.1/" xmlns:olac10="http://www.language-archives.org/OLAC/1.0/">
	<xsl:output method="html" version="4.0"/>
	<xsl:template match="/record/header">
		<!-- do nothing -->
	</xsl:template>
	<xsl:template match="/record/metadata/olac11:olac|/record/metadata/olac10:olac">
		<xsl:variable name="title">
			<xsl:choose>
				<xsl:when test="dc:title|dcterms:alternative">
					<xsl:value-of select="(dc:title|dcterms:alternative)[1]"/>
				</xsl:when>
				<xsl:otherwise>No title</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<html>
			<head>
				<title>
					<xsl:value-of select="$title"/>
				</title>
				<script type="text/javascript" src="/js/gatrack.js"></script>
			</head>
			<body>
				<hr style="color: black"/>
				<h1>
					<xsl:value-of select="$title"/>
				</h1>
				<hr style="color: black"/>
				<table cellpadding="1" cellspacing="6">
					<xsl:apply-templates/>
					<tr><td></td><td></td></tr>
					<tr><td></td><td></td></tr>
					<tr>
						<td bgcolor="silver"><b>&#160;OAI Identifier&#160;</b></td>
						<td bgcolor="#f0f0f0"><xsl:value-of select="/record/header/identifier"/></td>
					</tr>
					<tr>
						<td bgcolor="silver"><b>&#160;Datestamp&#160;</b></td>
						<td bgcolor="#f0f0f0"><xsl:value-of select="/record/header/datestamp"/></td>
					</tr>
				</table>
				<hr style="color: black"/>
				<p>
					<small>
						<xsl:text>This resource description follows the </xsl:text>
						<a href="http://www.language-archives.org/OLAC/metadata.html">metadata standard</a>
						<xsl:text> of the </xsl:text>
						<a href="http://www.language-archives.org/">Open Language Archives Community</a>
						<xsl:text>.</xsl:text>
					</small>
				</p>
			</body>
		</html>
	</xsl:template>
	<xsl:template match="/record/metadata/olac11:olac/*|/record/metadata/olac10:olac/*">
		<xsl:variable name="tag">
			<xsl:choose>
				<xsl:when test="contains(name(),':')">
					<xsl:value-of select="substring-after(name(), ':')"/>
				</xsl:when>
				<xsl:otherwise>
					<xsl:value-of select="name()"/>
				</xsl:otherwise>
			</xsl:choose>
		</xsl:variable>
		<xsl:variable name="label">
			<xsl:call-template name="capitalize">
				<xsl:with-param name="label">
					<xsl:value-of select="$tag"/>
				</xsl:with-param>
			</xsl:call-template>
		</xsl:variable>
		<xsl:variable name="code">
			<xsl:value-of select="translate(@olac11:code ,'_', ' ')"/>
			<xsl:value-of select="translate(@olac10:code ,'_', ' ')"/>
		</xsl:variable>
		<tr valign="top">
			<td bgcolor="silver">
				<b>
					<xsl:text disable-output-escaping="yes">&#160;</xsl:text>
					<xsl:if test="name() != name(preceding-sibling::*[1])">
						<xsl:value-of select="$label"/>
					</xsl:if>
					<xsl:text disable-output-escaping="yes">&#160;</xsl:text>
				</b>
			</td>
			<td bgcolor="#f0f0f0">
				<xsl:choose>
					<xsl:when test="@xsi:type='olac:discourse-type'">
						<xsl:call-template name="olac-display-format">
							<xsl:with-param name="label">Discourse type</xsl:with-param>
							<xsl:with-param name="primaryCode">
								<xsl:call-template name="capitalize">
									<xsl:with-param name="label">
										<xsl:value-of select="@olac11:code"/>
										<xsl:value-of select="@olac10:code"/>
									</xsl:with-param>
								</xsl:call-template>
							</xsl:with-param>
						</xsl:call-template>
					</xsl:when>
					<xsl:when test="@xsi:type='olac:language'">
						<xsl:call-template name="olac-display-format">
							<xsl:with-param name="code">
								<xsl:value-of select="$code"/>
							</xsl:with-param>
							<xsl:with-param name="primaryCode">
								<xsl:value-of select="document('LanguageCodes.xsd')//xs:enumeration[@value=$code]//xs:documentation"/>
							</xsl:with-param>
						</xsl:call-template>
					</xsl:when>
					<xsl:when test="@xsi:type='olac:linguistic-field'">
						<xsl:call-template name="olac-display-format">
							<xsl:with-param name="primaryCode">
								<xsl:call-template name="capitalize">
									<xsl:with-param name="label">
										<xsl:value-of select="$code"/>
									</xsl:with-param>
								</xsl:call-template>
							</xsl:with-param>
						</xsl:call-template>
					</xsl:when>
					<xsl:when test="@xsi:type='olac:linguistic-type'">
						<xsl:call-template name="olac-display-format">
							<xsl:with-param name="label">Linguistic type</xsl:with-param>
							<xsl:with-param name="primaryCode">
								<xsl:call-template name="capitalize">
									<xsl:with-param name="label">
										<xsl:value-of select="$code"/>
									</xsl:with-param>
								</xsl:call-template>
							</xsl:with-param>
						</xsl:call-template>
					</xsl:when>
					<xsl:when test="@xsi:type='olac:role'">
						<xsl:call-template name="olac-display-format">
							<xsl:with-param name="secondaryCode">
								<xsl:value-of select="$code"/>
							</xsl:with-param>
						</xsl:call-template>
					</xsl:when>
					<xsl:when test="@xsi:type='dcterms:IMT'">
						<xsl:call-template name="olac-display-format">
							<xsl:with-param name="label">MIME type</xsl:with-param>
						</xsl:call-template>
					</xsl:when>
					<xsl:otherwise>
						<xsl:call-template name="element-content"/>
					</xsl:otherwise>
				</xsl:choose>
			</td>
		</tr>
	</xsl:template>
	<xsl:template name="capitalize">
		<xsl:param name="label"/>
		<xsl:value-of select="concat( translate(substring($label,1,1),  'abcdefghijklmnopqrstuvwxyz', 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'), substring($label, 2, string-length($label)-1))"/>
	</xsl:template>
	<xsl:template name="olac-display-format">
		<xsl:param name="label"/>
		<xsl:param name="code"/>
		<xsl:param name="primaryCode"/>
		<xsl:param name="secondaryCode"/>
		<xsl:if test="$label">
			<xsl:value-of select="$label"/>
			<xsl:text>: </xsl:text>
		</xsl:if>
		<xsl:choose>
			<xsl:when test="$primaryCode != ''">
				<xsl:value-of select="$primaryCode"/>
				<xsl:if test=". != ''">
					<xsl:text> / </xsl:text>
					<xsl:call-template name="element-content"/>
				</xsl:if>
				<xsl:if test="$code != ''">
					<xsl:value-of select="concat( ' [', $code, ']' )"/>
				</xsl:if>
			</xsl:when>
			<xsl:when test="$secondaryCode != ''">
				<xsl:call-template name="element-content"/>
				<xsl:text> [</xsl:text>
				<xsl:value-of select="$secondaryCode"/>
				<xsl:text>]</xsl:text>
			</xsl:when>
			<xsl:otherwise>
				<xsl:call-template name="element-content"/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
	<xsl:template name="element-content">
		<xsl:choose>
			<xsl:when test="starts-with(.,'http://')">
				<a href="{.}">
					<xsl:value-of select="."/>
				</a>
			</xsl:when>
			<xsl:otherwise>
				<xsl:value-of select="."/>
			</xsl:otherwise>
		</xsl:choose>
	</xsl:template>
</xsl:stylesheet>
